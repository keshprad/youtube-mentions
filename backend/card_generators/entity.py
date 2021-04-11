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
    try:    
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(e)
        return []

    lines = []

    for each in transcript:
        line = { 'start': each['start'], 'text': each['text'].replace('-', ' ') }
        lines.append(line)

    cards = create_entity_cards(lines)
    return cards

def create_entity_cards(lines: List) -> List:
    nlp = en_core_web_sm.load()

    categories = {"PERSON": "person", "LOC": "place", "GPE": "place"}

    ents = {}
    size = len(lines)

    for i in range(size):
        doc = nlp(lines[i]['text'])

        for ent in doc.ents:
            if ent.label_ in categories.keys():
                name = ent.text
                found = wikipedia.search(name, results=1)[0]

                if found not in ents.keys():
                    info = get_wiki_info(found)
                    
                    if 'may refer to' not in info['summary']:
                        ents[found] = {
                            'name': found,
                            'card_type': categories[ent.label_],
                            'time': {'start': lines[i]['start']},
                            'image': info['image'],
                            'links': {'wikipedia': info['link']},
                            'summary': info['summary'],
                        }
                        
    cards = list(ents.values())

    return cards