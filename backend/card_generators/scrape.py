from typing import List
from pyppeteer import launch
import wikipedia


async def scrape_game_music(yt_url: str) -> List[dict]:
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(yt_url, {
        'waitUntil': 'networkidle0'
    })

    cards = []
    # Query for categories (used for finding game name)
    cat_elems = await page.querySelectorAll('a#endpoint-link div#title')
    # Query for music name and artist

    game = await find_game(cat_elems, page)
    print(game)
    await browser.close()

    # if game is not None:
    #     game_card = create_game_card(game)
    # cards.append(game_card)


async def find_game(cat_elems, page):
    if len(cat_elems) == 2:
        category = await page.evaluate('(element) => element.textContent', cat_elems[1])
        if category.lower() == "gaming":
            game = await page.evaluate('(element) => element.textContent', cat_elems[0])
            return game
    return None


def create_game_card(game):
    game_wiki = wikipedia.page(game)
    wiki_summary = wikipedia.summary(game, sentences=2)

    # Find Artist's wiki page and get info

    game_card = {
        'card_type': 'game',
        'time': {'start': 0},
        'name': game,
        # 'image': serialized.avatar,
        # 'genre': serialized.genres_primary,
        'links': {
            'wikipedia': game_wiki.url,
        },
        'summary': wiki_summary,
    }
    print(game_card)
    return game_card
