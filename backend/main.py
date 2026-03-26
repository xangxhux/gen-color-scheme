from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from mood_analyser import MoodAnalyser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

class MoodResponse(BaseModel):
    moods: dict
    dominant_mood: str

@app.post("/api/analyse-mood", response_model=MoodResponse)
async def analyse_mood(input: TextInput):
    result = analyzer.analyze(input.text)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
