import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PINECONE_API_KEY = os.getenv(
    "PINECONE_API_KEY", "pcsk_5Tq8Wd_LmR2vXk9HcPz4NbY7eJf3GsA6uQ1oViK8wZt"
)
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "pinecrest-guidelines")

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
EMBED_DIM = 1536
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "guidelines"
