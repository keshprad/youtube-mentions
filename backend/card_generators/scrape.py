from card_generators.shazam import create_song_card
from typing import List
from pyppeteer import launch
import wikipedia
from card_generators.wiki_helper import get_wiki_image
from shazamio import Shazam
from card_generators.shazam import create_artist_cards


async def scrape_game_music(yt_url: str) -> List[dict]:
    browser = await launch()
    page = await browser.newPage()
    await page.goto(yt_url, {
        'waitUntil': 'networkidle0'
    })
    showmore = await page.querySelector('paper-button#more')
    if showmore is not None:
        await showmore.click()

    # Query for categories (used for finding game name)
    cat_elems = await page.querySelectorAll('a#endpoint-link div#title')
    game = await find_game(cat_elems, page)
    # Query for music name and artist
    music_elems = await page.querySelectorAll('div#collapsible > .style-scope > *')
    songs = await find_songs(music_elems, page)

    # Close browser
    await browser.close()

    cards = []
    if game is not None:
        game_card = create_game_card(game)
        cards.append(game_card)
    if len(songs) > 0:
        for song in songs:
            song_info = await shazam_search(song)
            if song_info is not None:
                song_card = create_song_card(song_info)
                cards.append(song_card)
                artist_card = await create_artist_cards(song_info['artists'])
                cards += artist_card
    return cards


async def find_game(cat_elems: List, page) -> str:
    if len(cat_elems) == 2:
        category = await page.evaluate('(element) => element.textContent', cat_elems[1])
        if category.lower() == "gaming":
            game = await page.evaluate('(element) => element.textContent', cat_elems[0])
            return game
    return None


def create_game_card(game: str) -> dict:
    # Find Game's wiki page and get info
    title = wikipedia.search(game, results=1)[0]
    wiki_page = wikipedia.page(title, auto_suggest=False)
    wiki_summary = wikipedia.summary(title, sentences=2, auto_suggest=False)

    game_card = {
        'card_type': 'game',
        'time': {'start': 0},
        'title': game,
        'image': get_wiki_image(wiki_page.url),
        'links': {
            'wikipedia': wiki_page.url,
        },
        'summary': wiki_summary,
    }
    return game_card


async def find_songs(music_elems: List, page) -> List[dict]:
    songs, i = [], 0
    while i < len(music_elems):
        row = await page.evaluate('(element) => element.textContent', music_elems[i])
        row = row.strip()
        if row.lower() == "song":
            title = await page.evaluate('(element) => element.textContent', music_elems[i+1])
            artist = await page.evaluate('(element) => element.textContent', music_elems[i+3])
            song = {
                'title': title.strip(),
                'artists': artist.strip().split(', '),
            }
            i += 3
            songs.append(song)
        i += 1
    return songs


async def shazam_search(song: dict) -> dict:
    shazam = Shazam()

    query = f"{song['title']} {' '.join(song['artists'])}"
    tracks = await shazam.search_track(query=query, limit=1)
    if 'tracks' in tracks:
        song_info = tracks['tracks']['hits'][0]
        return song_info


def create_song_card(song):
    song_card = {
        'card_type': 'song',
        'time': {'start': 0},
        'title': song['heading']['title'],
        'artists': song['heading']['subtitle'],
        'image': song['images']['default'],
        'links': {
            'shazam': song['url'],
        },
    }
    if "spotify" in song['streams']:
        song_card['links']['spotify'] = song['streams']['spotify']['actions'][0]['uri']
    if "apple" in song['stores']:
        song_card['links']['apple'] = song['stores']['apple']['actions'][0]['uri']

    return song_card
