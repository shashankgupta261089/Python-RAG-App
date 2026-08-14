from helpers.settings import CHAT_MODEL, DOCUMENT_SOURCE, EMBEDDING_MODEL
from helpers.storage import openai_client, supabase_client


def embed_text(text: str) -> list:
    # Embed the user question into the same vector space as the records.
    response = openai_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


def retrieve(question: str, top_k: int = 4) -> list:
    # Convert the question into a vector.
    query_embedding = embed_text(question)

    # Keep retrieval scoped to this sample document.
    metadata_filter = {"source": DOCUMENT_SOURCE}

    # match_documents is the SQL function created earlier.
    result = supabase_client().rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "filter": metadata_filter,
        },
    ).execute()

    return result.data or []


def source_label(metadata: dict) -> str:
    # Build a readable source label from metadata.
    return metadata.get("citation", "Unknown source")


def format_context(retrieved_rows: list) -> str:
    # Turn retrieved rows into the exact context text sent to the answer model.
    context_parts = []

    for row in retrieved_rows:
        label = source_label(row["metadata"])
        context_parts.append(f"Citation: {label}\n{row['content']}")

    return "\n\n".join(context_parts)


def answer_question(question: str, retrieved_rows: list) -> str:
    # Generate a grounded answer from retrieved context only.
    if not retrieved_rows:
        return "I could not find an answer in the uploaded PDF content."

    prompt_context = format_context(retrieved_rows)

    response = openai_client().chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer only from the provided context. "
                    "Cite the answer using the Citation labels from the context along with the Source, "
                    "If the answer is missing, greet and reply politely to ask from source."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{prompt_context}\n\nQuestion: {question}" + f" Source: {DOCUMENT_SOURCE}",
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content
