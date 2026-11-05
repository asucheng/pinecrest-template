from langsmith import traceable

from pinecrest import config
from pinecrest.clients import openai_client

PROMPT = """You are the Pinecrest Property Management resident assistant.
Answer the resident's question using ONLY the guideline excerpts below.
If the excerpts do not contain the exact answer, reply exactly:
"I'm sorry, I don't have that information. Please contact the front desk."
Always reply in English.
Quote every relevant rule in full, including section numbers, so the resident has the complete policy.

Guideline excerpts:
{context}

Resident question: {question}"""


@traceable(name="generate")
def generate(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(f"[{c['source']}]\n{c['text']}" for c in chunks)
    resp = openai_client().chat.completions.create(
        model=config.CHAT_MODEL,
        messages=[{"role": "user", "content": PROMPT.format(context=context, question=question)}],
        temperature=0,
    )
    return resp.choices[0].message.content or ""
