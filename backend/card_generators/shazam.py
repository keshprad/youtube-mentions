from typing import List
from shazamio import Shazam, FactoryArtist
import wikipedia
import json


async def identify_song(audio_path: str) -> List[dict]:
    """Use Shazam API to find artist & song, then create cards for them."""
    shazam = Shazam()

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
        artist_wiki = wikipedia.page(serialized.name)
        wiki_summary = wikipedia.summary(serialized.name, sentences=2)

        artist_card = {
            'card_type': 'artist',
            'time': {'start': 0},
            'name': serialized.name,
            'image': serialized.avatar,
            'genre': serialized.genres_primary,
            'links': {
                'shazam': f"https://www.shazam.com/artist/{artist['id']}/{serialized.alias}",
                'wikipedia': artist_wiki.url,
            },
            'summary': wiki_summary,
        }
        artist_cards.append(artist_card)
    return artist_cards
