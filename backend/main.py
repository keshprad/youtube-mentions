from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import generate_cards
import json


app = FastAPI()
origins = ["http://localhost:5000"]
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def root():
    return {"Hello": "world"}


@app.get("/cards/{vid_id}")
async def get_cards(vid_id: str):
    cards = []
    cards = await generate_cards.generate(vid_id)

    # Test Cards...
    # cards = [
    #     {
    #         "card_type": "artist",
    #         "time": {
    #             "start": 0
    #         },
    #         "name": "Rick Astley",
    #         "image": "https://is3-ssl.mzstatic.com/image/thumb/Features124/v4/cf/29/7a/cf297a7e-d30e-0fa8-0028-a4415f4be0af/pr_source.png/800x800bb.jpeg",
    #         "genre": "Pop",
    #         "links": {
    #             "shazam": "https://www.shazam.com/artist/4300/rick-astley",
    #             "wikipedia": "https://en.wikipedia.org/wiki/Rick_Astley",
    #         },
    #         "summary": "Richard Paul Astley (born 6 February 1966) is a British singer, songwriter and radio personality. He rose to fame through his association with the production trio Stock Aitken Waterman; his 1987 recording of their song \"Never Gonna Give You Up\" was a number 1 hit single in 25 countries, winning the 1988 Brit Award for Best British Single."
    #     },
    #     {
    #         "card_type": "song",
    #         "time": {
    #             "start": 0
    #         },
    #         "title": "Never Gonna Give You Up",
    #         "artists": "Rick Astley",
    #         "image": "https://is5-ssl.mzstatic.com/image/thumb/Music114/v4/e5/3a/da/e53ada8e-bf49-da8a-8f6b-9183a5150405/859381157694.jpg/800x800bb.jpeg",
    #         "links": {
    #             "shazam": "https://www.shazam.com/track/357027/never-gonna-give-you-up",
    #             "apple": "https://music.apple.com/gb/album/never-gonna-give-you-up/1558533900?i=1558534271&mttnagencyid=769459046716559743&mttnsiteid=125115&mttn3pid=a_custom_779816081798873874&mttnsub1=Shazam_ios&mttnsub2=5348615A-616D-3235-3830-44754D6D5973&itscg=30201&app=music&itsct=Shazam_ios",
    #             "spotify": "spotify:track:4uLU6hMCjMI75M1A2tKUQC"
    #         }
    #     },
    #     {
    #         "card_type": "song",
    #         "time": {
    #             "start": 1
    #         },
    #         "title": "Never Gonna Give You Up",
    #         "artists": "Rick Astley",
    #         "image": "https://is5-ssl.mzstatic.com/image/thumb/Music114/v4/e5/3a/da/e53ada8e-bf49-da8a-8f6b-9183a5150405/859381157694.jpg/800x800bb.jpeg",
    #         "links": {
    #             "shazam": "https://www.shazam.com/track/357027/never-gonna-give-you-up",
    #             "apple": "https://music.apple.com/gb/album/never-gonna-give-you-up/1558533900?i=1558534271&mttnagencyid=769459046716559743&mttnsiteid=125115&mttn3pid=a_custom_779816081798873874&mttnsub1=Shazam_ios&mttnsub2=5348615A-616D-3235-3830-44754D6D5973&itscg=30201&app=music&itsct=Shazam_ios",
    #         }
    #     },
    # ]

    with open('test_out.json', 'w') as file:
        json.dump(cards, file, indent=2)

    # Return cards in reverse order
    return sorted(cards, key=lambda card: card['time']['start'], reverse=True)
