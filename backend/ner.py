import spacy
import en_core_web_sm
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
import wikipedia
import helper

id = 'LIYiThAyY8s'

# def get_id(url):
#     parsed = parse.urlparse(url)
#     if 'youtube' in parsed.hostname: return parse.parse_qs(parsed.query)['v'][0]
#     if 'youtu.be' in parsed.hostname: return parsed.path[1:]
#     return None

transcript = YouTubeTranscriptApi.get_transcript(id)

nlp = en_core_web_sm.load()

text = ' '.join([ line['text'].replace('-', ' ') for line in transcript ])

starts = [ line['start'] for line in transcript ]

doc = nlp(text)

ents = {}
for i in range(len(doc.ents)):
    categories = ("PERSON", "LOC", "GPE")
    if doc.ents[i].label_ in categories:
        name = doc.ents[i].text
        found = wikipedia.search(name, results=1)[0]

        if found not in ents.keys():
            try:
                page = wikipedia.page(found, auto_suggest=False )
            except wikipedia.DisambiguationError as e:
                found = e.options[0]
                page = wikipedia.page(found, auto_suggest=False )
                
            ents[found] = {
                'name': found,
                'card_type': doc.ents[i].label_,
                'time': {'start': starts[i]},
                'image': helper.get_wiki_image(found),
                'links': { 'wikipedia': page.url },
                'summary': wikipedia.summary(found, sentences=2, auto_suggest=False ),
            }
            print(ents[found])


print(list(ents.values()))
