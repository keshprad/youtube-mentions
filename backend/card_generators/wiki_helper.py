import requests
import json
from bs4 import BeautifulSoup

WIKI_REQUEST = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=&format=json&redirects=&exsentences=2&titles='

def get_wiki_info(title : str) -> str:
    response  = requests.get(WIKI_REQUEST + title)
    json_data = json.loads(response.text)

    summary = list(json_data['query']['pages'].values())[0]['extract'].split('\n')[0]

    print("wiki_helper.py: " + summary)

    link = "https://en.wikipedia.org/wiki/" + title.replace(' ', '_')

    response = requests.get(link)
    soup = BeautifulSoup(response.text)
    
    image = soup.find("meta",  property="og:image")
    image = image['content'] if image else None

    print("wiki_helper.py: " + image)

    return { 'summary': summary + '..', 'image': image, 'link': link }