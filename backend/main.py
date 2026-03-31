from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from colors import COLOR_DATA
from mood_analyser import Config

from mood_analyser import MoodAnalyser, MoodEmbedding

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_methods=["*"],
        allow_headers=["*"],
        )

# Initialize model once on startup
analyser = MoodAnalyser(config=Config(), color_data=COLOR_DATA)

class TextInput(BaseModel):
    mood_text: str

class MoodResponse(BaseModel):
    theme_colors: list[dict[str,str]]
    theme_css: str 

@app.post("/api/analyse-mood", response_model=MoodResponse)
def analyse_mood(input: TextInput) -> MoodResponse:
    result = analyser.analyse_mood(input.mood_text)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
