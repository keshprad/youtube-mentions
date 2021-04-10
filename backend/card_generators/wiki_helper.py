from bs4 import BeautifulSoup


def get_wiki_image(html: str) -> str:
    soup = BeautifulSoup(html)
    box = soup.find('td', class_="infobox-image")
    if box is not None:
        return "https:" + box.find('img')['src']

    return None
