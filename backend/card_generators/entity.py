import spacy
import en_core_web_sm
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
from helper import get_wiki_image
import wikipedia


URL = 'https://youtu.be/LIYiThAyY8s'

# def get_id(url):
#     parsed = parse.urlparse(url)
#     if 'youtube' in parsed.hostname: return parse.parse_qs(parsed.query)['v'][0]
#     if 'youtu.be' in parsed.hostname: return parsed.path[1:]
#     return None

async def identify_entities(video_id : str) -> List:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = ' '.join([ line['text'].replace('-', ' ') for line in transcript ])

    cards = create_entity_cards(text)
    return cards

def create_entity_cards(text : str, transcript : List) -> List:
    nlp = en_core_web_sm.load()
    doc = nlp(text)

    ents = {}
    for i in range(len(doc.ents) - 1, -1, -1):
        categories = ("PERSON", "LOC", "GPE")
        if doc.ents[i].label_ in categories and len(doc.ents[i].text.split()) > 1:
            name = doc.ents[i].text
            found = wikipedia.search(name, results=1)[0]
            page = wikipedia.page(found, auto_suggest=False )

            ents[name] = {
                'name': name,
                'card_type': doc.ents[i].label_,
                'time': {'start': transcript[i]['start']},
                'image': get_wiki_image(found),
                'links': { 'wikipedia': page.url },
                'summary': wikipedia.summary(found, sentences=2, auto_suggest=False ),
            }

    cards = list(ents.values())

    return cards