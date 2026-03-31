import os
from typing import TypedDict
import numpy as np
from gradio_client import Client
from sentence_transformers import SentenceTransformer, util
from huggingface_hub import login

# --- CONFIGURATION ---
class Config:
    """Configuration settings for the application."""
    EMBEDDING_MODEL_ID = "google/embeddinggemma-300M"
    # PROMPT_NAME = "STS"
    TOP_K = 5
    HF_TOKEN = os.getenv('HF_TOKEN')

class MoodEmbedding(TypedDict):
    label: str
    score: float

# --- CORE LOGIC ---
# Encapsulated in a class to manage state (model, embeddings) cleanly.
class MoodAnalyser:
    def __init__(self, config: Config, color_data: list[dict[str, any]]):
        self.config = config
        self.color_data = color_data
        self._login_to_hf()
        self.embedding_model = self._load_model()
        self.color_embeddings = self._precompute_color_embeddings()

    def _debug(self, message: str, content):
        with open("debug.log", "a") as f:
            if isinstance(content, (dict, list, tuple)):
                content_str = json.dumps(content, indent=2, default=str, ensure_ascii=False)
            else:
                content_str = str(content)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp}\t{message}\t:\t{content_str}\n")


    def _login_to_hf(self):
        """Logs into Hugging Face Hub if a token is provided."""
        print(f'found secret token '+self.config.HF_TOKEN)
        if self.config.HF_TOKEN:
            print("Logging into Hugging Face Hub...")
            login(token=self.config.HF_TOKEN)
        else:
            print("HF_TOKEN not found. Proceeding without login.")
            print("Note: This may fail if the model is gated.")

    def _load_model(self) -> SentenceTransformer:
        """Loads the Sentence Transformer model."""
        print(f"Initializing embedding model: {self.config.EMBEDDING_MODEL_ID}...")
        try:
            return SentenceTransformer(self.config.EMBEDDING_MODEL_ID)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def _precompute_color_embeddings(self) -> np.ndarray:
        """Generates and stores embeddings for the color descriptions."""
        print("Pre-computing embeddings for color palette...")
        color_texts = [
            f"{color['name']}, {color['description']}"
            for color in self.color_data
        ]
        embeddings = self.embedding_model.encode(
            color_texts,
            prompt_name=self.config.PROMPT_NAME
        )
        print("Embeddings computed successfully.")
        return embeddings

    def _get_text_color_for_bg(self, hex_color: str) -> str:
        """
        Calculates the luminance of a hex color and returns black ('#000000')
        or white ('#FFFFFF') for the best text contrast.
        """
        hex_color = hex_color.lstrip('#')
        try:
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            luminance = (0.299 * r + 0.587 * g + 0.114 * b)
            return '#000000' if luminance > 150 else '#FFFFFF'
        except (ValueError, IndexError):
            return '#000000' # Default to black on invalid hex

    def _generate_palette_and_theme(self, mood_data: dict) -> tuple[str, str]:
        """Generates a color palette in CSS values based on the given mood"""
       return ("HI", "HI")


    def analyse_mood(self, mood_text: str) -> dict:
        """Returns mood scores for the given text"""
        mood_embedding = self.embedding_model.encode(mood_text, prompt_name=self.config.PROMPT_NAME)
        print(mood_embedding)
        top_hits = util.semantic_search(
                mood_embedding, self.color_embeddings, top_k=self.config.TOP_K
                )[0]
        print(top_hits)

        # Sample response 
        return {
                'moods': {'asdf':123},
                'dominant_mood': {"happy": 1.0},
                'mood_palette': '' 
                }

