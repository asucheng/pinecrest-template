from langsmith import traceable

from pinecrest import config
from pinecrest.clients import embed, pinecone_client

TOP_K = 3


@traceable(name="retrieve")
def retrieve(question: str, top_k: int = TOP_K) -> list[dict]:
    index = pinecone_client().Index(config.PINECONE_INDEX)
    res = index.query(vector=embed([question])[0], top_k=top_k, include_metadata=True)
    results = []
    for m in res.matches:
        md = m.metadata or {}
        results.append({"text": md.get("text", ""), "source": md.get("source", ""), "score": m.score})
    return results
