from helpers.settings import DOCUMENT_SOURCE


def build_rag_records(page_inventory: list) -> list:
    # Convert the inventory into simple text records for RAG.
    rag_records = []

    for page in page_inventory:
        page_number = page["page_number"]
        page_title = page["title"]

        if page["processed_text"]:
            rag_records.append({
                "content": f"Page {page_number}: {page_title}\n{page['processed_text']}",
                "metadata": {
                    "source": DOCUMENT_SOURCE,
                    "citation": f"Page {page_number} text",
                },
            })

        for table in page["tables"]:
            if table["text"]:
                rag_records.append({
                    "content": f"Page {page_number}: {page_title}\nTable: {table['title']}\n{table['text']}",
                    "metadata": {
                        "source": DOCUMENT_SOURCE,
                        "citation": f"Page {page_number} table",
                    },
                })

        if page["image_text"]:
            rag_records.append({
                "content": f"Page {page_number}: {page_title}\nImage text:\n{page['image_text']}",
                "metadata": {
                    "source": DOCUMENT_SOURCE,
                    "citation": f"Page {page_number} image",
                },
            })

    return rag_records
