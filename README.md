# Pinecrest Resident Assistant

Chatbot that answers resident questions from the Pinecrest guidelines.

## Run

```
uv sync
cp .env.example .env   # add keys
uv run python -m pinecrest.ingest
uv run uvicorn pinecrest.app:app --port 8080
```

Open http://localhost:8080
