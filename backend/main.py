from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from mood_analyser import MoodAnalyser, MoodEmbedding

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model once on startup
analyser = MoodAnalyser()

class TextInput(BaseModel):
    mood_text: str

class MoodResponse(BaseModel):
    moods: dict
    dominant_mood: str
    mood_palette: dict[str, dict]

@app.post("/api/analyse-mood", response_model=MoodResponse)
async def analyse_mood(input: TextInput) -> MoodResponse:
    result = analyser.analyse_mood(input.mood_text)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
