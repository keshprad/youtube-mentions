from typing import List
import youtube_dl
from card_generators import shazam, entity, scrape


def get_yt_url(
    vid_id: str) -> str: return f"https://www.youtube.com/watch?v={vid_id}"


async def generate(vid_id: str) -> List[dict]:
    """Calls all card_generators and returns list of cards (represented as dicts)"""
    yt_url = get_yt_url(vid_id)
    cards = []

    # download audio and video
    print("// [1] Downloading Audio & Video //")
    dl_audio_video(vid_id)

    print("// [2] Detecting Music //")
    shazam_cards = await shazam.identify_song(f'downloads/a_{vid_id}.m4a')
    scrape_songs = len(shazam_cards) == 0
    cards += shazam_cards

    print("// [3] Detecting Entities //")
    # ent_cards = await entity.identify_entities(vid_id)
    # cards += ent_cards

    print("// [4] Scraping for Games & Music //")
    scraped_cards = await scrape.scrape_game_music(yt_url, scrape_songs=scrape_songs)
    cards += scraped_cards
    return cards


def dl_audio_video(vid_id: str):
    """Downloads audio and video files from specified YouTube video"""
    yt_url = get_yt_url(vid_id)

    # Download video
    ydl_video_opts = {
        'format': 'mp4',
        'outtmpl': f'downloads/v_{vid_id}.mp4',
    }
    with youtube_dl.YoutubeDL(ydl_video_opts) as ydl:
        ydl.download([yt_url])

    # Download audio
    ydl_audio_opts = {
        'format': 'm4a',
        'outtmpl': f'downloads/a_{vid_id}.m4a',
    }
    with youtube_dl.YoutubeDL(ydl_audio_opts) as ydl:
        ydl.download([yt_url])

    # Meta Info
    # meta = ydl.extract_info(yt_url, download=False)
