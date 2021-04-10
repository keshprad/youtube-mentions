import requests
import json
from bs4 import BeautifulSoup

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(html : str) -> str:
    # response  = requests.get(WIKI_REQUEST + title)
    # json_data = json.loads(response.text)
    # print(json_data)
    # page_data = list(json_data['query']['pages'].values())[0]
    # # pprint.pprint(json_data)
    # # print(title + ": " + str(page_data))

    # if 'original' in page_data:
    #     img_link = page_data['original']['source']
    #     return img_link

    soup = BeautifulSoup(html)
    box = soup.find('td', class_="infobox-image")
    if box is not None: 
        return "https:" + box.find('img')['src']

    return None