from dotenv import load_dotenv
from google import genai
import os

#load SECRET KEYS from .env, optional for gemini apis as it can read directly from env
load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

google_genai_client = genai.Client(api_key=GEMINI_API_KEY)
