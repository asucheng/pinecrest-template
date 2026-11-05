from pinecone import ServerlessSpec

from pinecrest import config
from pinecrest.clients import embed, pinecone_client

CHUNK_SIZE = 300
BATCH = 64


def load_documents() -> list[tuple[str, str]]:
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted(config.DATA_DIR.rglob("*.md"))]


def chunk_text(text: str, size: int = CHUNK_SIZE) -> list[str]:
    return [text[i : i + size] for i in range(0, len(text), size)]


def ensure_index() -> None:
    pc = pinecone_client()
    if config.PINECONE_INDEX not in pc.list_indexes().names():
        pc.create_index(
            name=config.PINECONE_INDEX,
            dimension=config.EMBED_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )


def main() -> None:
    ensure_index()
    index = pinecone_client().Index(config.PINECONE_INDEX)

    records = []
    for name, text in load_documents():
        for i, chunk in enumerate(chunk_text(text)):
            records.append({"id": f"{name}-{i}", "text": chunk, "source": name})

    for start in range(0, len(records), BATCH):
        batch = records[start : start + BATCH]
        vectors = embed([r["text"] for r in batch])
        index.upsert(
            vectors=[
                {"id": r["id"], "values": v, "metadata": {"text": r["text"], "source": r["source"]}}
                for r, v in zip(batch, vectors)
            ]
        )
    print(f"Upserted {len(records)} chunks into {config.PINECONE_INDEX}")


if __name__ == "__main__":
    main()
