from fastapi import FastAPI
from pydantic import BaseModel
from graph import graph
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="ClipForge API", version="1.0.0")

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

app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs",
)