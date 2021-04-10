from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import generate_cards


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
    try:
        cards += await generate_cards.generate(vid_id)
    except Exception as e:
        print(f"Error: {e}")
    return cards
