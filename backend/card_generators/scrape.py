from typing import List
from pyppeteer import launch
import wikipedia


async def scrape_game_music(yt_url: str) -> List[dict]:
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(yt_url, {
        'waitUntil': 'networkidle0'
    })

    cards = []
    # Query for categories (used for finding game name)
    cat_elems = await page.querySelectorAll('a#endpoint-link div#title')
    game = await find_game(cat_elems, page)
    # Query for music name and artist
    music_elems = await page.querySelectorAll('div#collapsible')
    music = await find_music(music_elems, page)
    await browser.close()

    if game is not None:
        game_card = create_game_card(game)
        cards.append(game_card)


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
    print(title)

    game_card = {
        'card_type': 'game',
        'time': {'start': 0},
        'name': game,
        # 'image': serialized.avatar,
        'links': {
            'wikipedia': wiki_page.url,
        },
        'summary': wiki_summary,
    }
    print(game_card)
    return game_card


async def find_music(music_elems: List, page) -> str:
    if len(music_elems) == 1:
        print("hello")
        music = await page.evaluate('(element) => element.textContent', music_elems[0])
        print(music)
    return None
