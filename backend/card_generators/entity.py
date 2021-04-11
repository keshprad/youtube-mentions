import spacy
import en_core_web_sm
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
from card_generators.wiki_helper import get_wiki_info
import wikipedia

# def get_id(url):
#     parsed = parse.urlparse(url)
#     if 'youtube' in parsed.hostname: return parse.parse_qs(parsed.query)['v'][0]
#     if 'youtu.be' in parsed.hostname: return parsed.path[1:]
#     return None

async def identify_entities(video_id: str) -> List:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    lines = [line['text'].replace('-', ' ') for line in transcript]

    cards = create_entity_cards(lines, [line['start'] for line in transcript])
    return cards


def create_entity_cards(lines: List, start_times: List) -> List:
    nlp = en_core_web_sm.load()

    categories = {"PERSON": "person", "LOC": "place", "GPE": "place"}

    ents = {}
    size = len(start_times)

    for i in range(size):
        doc = nlp(lines[i])

        for ent in doc.ents:
            if ent.label_ in categories.keys():
                name = ent.text
                found = wikipedia.search(name, results=1)[0]

                if found not in ents.keys():
                    info = get_wiki_info(found)

                    ents[found] = {
                        'name': found,
                        'card_type': categories[ent.label_],
                        'time': {'start': start_times[i]},
                        'image': info['image'],
                        'links': {'wikipedia': info['link']},
                        'summary': info['summary'],
                    }
    cards = list(ents.values())

    return cards
