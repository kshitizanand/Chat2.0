from fastapi import FastAPI, Form
from src.gemini import google_genai_client
from google.genai import errors

import time

from src.db import Conversation, get_async_session, create_db_and_table
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Up and running!"}

@app.get("/models")
def get_models():
    model_list = []
    for m in google_genai_client.models.list():
        for action in m.supported_actions:
            if action == "generateContent":
                model_list.append(m.name)
    
    return {"response":  model_list}

@app.post("/ask")
def ask_ai(question: str = Form(...), ):
    print(f"Got a query: {question}")
    start = time.perf_counter()
    try:
        response = google_genai_client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=question
        )
    except errors.APIError as e:
        print(e.code)
        print(e.message)
        return {"response": e.message}

    time_taken = time.perf_counter() - start
    print(f"time taken in Gemini API call: {time_taken:0.2f}s")
    print(f"Sending response: {response.text}")
    return {"response": response.text}
