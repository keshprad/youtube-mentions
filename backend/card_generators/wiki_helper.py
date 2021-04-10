import requests
import json

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(title : str) -> str:
    response  = requests.get(WIKI_REQUEST + title)
    json_data = json.loads(response.text)
    page_data = list(json_data['query']['pages'].values())[0]
    # pprint.pprint(json_data)
    # print(title + ": " + str(page_data))

    if 'original' in page_data:
        img_link = page_data['original']['source']
        return img_link

    return None