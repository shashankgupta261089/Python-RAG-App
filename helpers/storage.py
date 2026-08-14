from openai import OpenAI
from supabase import create_client

from helpers.settings import (
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
    SUPABASE_KEY,
    SUPABASE_URL,
    TABLE_NAME,
)


def require_config() -> None:
    missing = []

    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    if not SUPABASE_URL or SUPABASE_URL.startswith("https://your-project"):
        missing.append("SUPABASE_URL")

    if not SUPABASE_KEY or SUPABASE_KEY.startswith("your_"):
        missing.append("SUPABASE_SERVICE_ROLE_KEY")

    if missing:
        raise RuntimeError("Missing values: " + ", ".join(missing))


def openai_client():
    return OpenAI(api_key=OPENAI_API_KEY)


def supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def embed_texts(texts: list) -> list:
    response = openai_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]


def save_records_to_supabase(chunked_records: list) -> int:
    texts = []
    for record in chunked_records:
        texts.append(record["content"])

    embeddings = embed_texts(texts)

    rows = []
    row_id = 1
    row_index = 0

    for record in chunked_records:
        rows.append({
            "id": row_id,
            "content": record["content"],
            "metadata": record["metadata"],
            "embedding": embeddings[row_index],
        })
        row_id = row_id + 1
        row_index = row_index + 1

    supabase_client().table(TABLE_NAME).delete().gte("id", 1).execute()
    result = supabase_client().table(TABLE_NAME).insert(rows).execute()
    return len(result.data or [])
