from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from langsmith import traceable
from pydantic import BaseModel

from pinecrest.generate import generate
from pinecrest.retrieve import retrieve

STATIC = Path(__file__).resolve().parents[2] / "static"

app = FastAPI(title="Pinecrest Resident Assistant")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@traceable(name="chat")
def answer(question: str) -> ChatResponse:
    chunks = retrieve(question)
    return ChatResponse(answer=generate(question, chunks), sources=[c["source"] for c in chunks])


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    return answer(req.question)


@app.get("/")
def home() -> FileResponse:
    return FileResponse(STATIC / "index.html")
