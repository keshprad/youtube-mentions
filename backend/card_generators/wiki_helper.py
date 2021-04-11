import requests
import json
from bs4 import BeautifulSoup


def get_wiki_info(title: str, sentences: int = 2) -> str:
    WIKI_REQUEST = f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=&format=json&redirects=&exsentences={sentences}&titles={title}'
    response = requests.get(WIKI_REQUEST)
    json_data = json.loads(response.text)

    summary = list(json_data['query']['pages'].values())[
        0]['extract']
    link = "https://en.wikipedia.org/wiki/" + title.replace(' ', '_')

    response = requests.get(link)
    soup = BeautifulSoup(response.text, features='html.parser')

    image = soup.find("meta",  property="og:image")
    image = image['content'] if image else None

    return {'summary': summary + '..', 'image': image, 'link': link}
