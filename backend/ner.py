import spacy
import en_core_web_sm
from urllib import parse
from spacy import displacy
from collections import Counter
from youtube_transcript_api import YouTubeTranscriptApi
import wikipedia
import pprint
from pathlib import Path

import helper

URL = 'https://youtu.be/LIYiThAyY8s'

def get_id(url):
    parsed = parse.urlparse(url)
    if 'youtube' in parsed.hostname: return parse.parse_qs(parsed.query)['v'][0]
    if 'youtu.be' in parsed.hostname: return parsed.path[1:]
    return None


transcript = YouTubeTranscriptApi.get_transcript(get_id(URL))

nlp = en_core_web_sm.load()

text = ' '.join([ line['text'].replace('-', ' ') for line in transcript ])

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
            'image': helper.get_wiki_image(found),
            'links': { 'wikipedia': page.url },
            'summary': wikipedia.summary(found, sentences=2, auto_suggest=False ),
        }


print(list(ents.values()))
