from functools import lru_cache

from langsmith.wrappers import wrap_openai
from openai import OpenAI
from pinecone import Pinecone

from pinecrest import config


@lru_cache
def openai_client() -> OpenAI:
    return wrap_openai(OpenAI(api_key=config.OPENAI_API_KEY))


@lru_cache
def pinecone_client() -> Pinecone:
    return Pinecone(api_key=config.PINECONE_API_KEY)


def embed(texts: list[str]) -> list[list[float]]:
    resp = openai_client().embeddings.create(model=config.EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]
