from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_rag_records(rag_records: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=420,
        chunk_overlap=80,
        separators=["\n\n", "\n", ". ", " "],
    )

    chunked_records = []
    record_number = 1

    for record in rag_records:
        chunks = splitter.split_text(record["content"])
        chunk_number = 1

        for chunk in chunks:
            chunk_metadata = record["metadata"].copy()
            chunk_metadata["record_number"] = record_number
            chunk_metadata["chunk_number"] = chunk_number

            chunked_records.append({
                "content": chunk,
                "metadata": chunk_metadata,
            })
            chunk_number = chunk_number + 1

        record_number = record_number + 1

    return chunked_records
