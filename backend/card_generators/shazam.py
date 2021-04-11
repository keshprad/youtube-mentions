from typing import List
from shazamio import Shazam, FactoryArtist
from pydub import AudioSegment
import wikipedia
from card_generators.wiki_helper import get_wiki_info
from tempfile import NamedTemporaryFile


async def identify_song(audio_path: str) -> List[dict]:
    """Use Shazam API to find artist & song, then create cards for them."""
    shazam = Shazam()

    audio = AudioSegment.from_file(audio_path)
    clip_length = 30
    if audio.duration_seconds > clip_length:
        clip = audio[:clip_length*1000]
        clip_file = NamedTemporaryFile(mode='w')
        clip.export(clip_file.name, format="mp3")
        song = await shazam.recognize_song(clip_file.name)
        clip_file.close()
    else:
        song = await shazam.recognize_song(audio_path)

    cards = []
    if len(song['matches']) > 0:
        # Generate cards for artists
        artist_cards = await create_artist_cards(artists=song['track']['artists'])
        cards += artist_cards

        # Generate card for song:
        song_card = create_song_card(song=song)
        cards.append(song_card)
    return cards


def create_song_card(song: dict) -> List[dict]:
    song_card = {
        'card_type': 'song',
        'time': {'start': 0},
        'title': song['track']['title'],
        'artists': song['track']['subtitle'],
        'image': song['track']['images']['coverarthq'],
        'links': {
            'shazam': song['track']['url'],
            'apple': song['track']['myshazam']['apple']['actions'][0]['uri'],
        },
    }
    if 'apple' in song['track']['myshazam']:
        song_card['links']['apple'] = song['track']['myshazam']['apple']['actions'][0]['uri']
    for provider in song['track']['hub']['providers']:
        if provider['type'] == 'SPOTIFY':
            song_card['links']['spotify'] = provider['actions'][0]['uri']
    return song_card


async def create_artist_cards(artists: List[dict]) -> List[dict]:
    shazam = Shazam()
    artist_cards = []
    for artist in artists:
        # Find basic info about artist
        about_artist = await shazam.artist_about(artist['id'])
        serialized = FactoryArtist(data=about_artist).serializer()

        # Find Artist's wiki page and get info
        wiki_title = wikipedia.search(serialized.name, results=1)[0]
        artist_wiki = get_wiki_info(wiki_title)

        artist_card = {
            'card_type': 'artist',
            'time': {'start': 0},
            'name': serialized.name,
            'image': serialized.avatar,
            'genre': serialized.genres_primary,
            'links': {
                'shazam': f"https://www.shazam.com/artist/{artist['id']}/{serialized.alias}",
                'wikipedia': artist_wiki['link'],
            },
            'summary': artist_wiki['summary'],
        }
        artist_cards.append(artist_card)
    return artist_cards
