from fastapi import FastAPI
from pydantic import BaseModel
from graph import graph
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="ClipForge API", version="1.0.0")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

class GenerateRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {
        "message": "Welcome to ClipForge API"
    }

@app.post("/generate")
def generate(request: GenerateRequest):

    result = graph.invoke({
        "url": request.url
    })

    return result

os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs",)