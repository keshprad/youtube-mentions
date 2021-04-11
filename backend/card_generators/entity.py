import spacy
import en_core_web_sm
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
from card_generators.wiki_helper import get_wiki_info
import wikipedia

URL = 'https://youtu.be/LIYiThAyY8s'

# def get_id(url):
#     parsed = parse.urlparse(url)
#     if 'youtube' in parsed.hostname: return parse.parse_qs(parsed.query)['v'][0]
#     if 'youtu.be' in parsed.hostname: return parsed.path[1:]
#     return None


async def identify_entities(video_id: str) -> List:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = ' '.join([line['text'].replace('-', ' ') for line in transcript])

    cards = create_entity_cards(text, [line['start'] for line in transcript])
    return cards


def create_entity_cards(text: str, start_times: List) -> List:
    nlp = en_core_web_sm.load()
    doc = nlp(text)

    categories = {"PERSON": "person", "LOC": "place", "GPE": "place"}

    ents = {}
    size = len(doc.ents)
    for i in range(size):
        if doc.ents[i].label_ in categories.keys():
            name = doc.ents[i].text
            found = wikipedia.search(name, results=1)[0]

            if found not in ents.keys():
                info = get_wiki_info(found)

                ents[found] = {
                    'name': found,
                    'card_type': categories[doc.ents[i].label_],
                    'time': {'start': start_times[i]},
                    'image': info['image'],
                    'links': {'wikipedia': info['link']},
                    'summary': info['summary'],
                }
    cards = list(ents.values())

    return cards
