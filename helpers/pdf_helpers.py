from openai import OpenAI
import base64
import pymupdf
import re

from helpers.settings import OPENAI_API_KEY, VISION_MODEL


def clean_text(text: str) -> str:
    # Normalize repeated spaces and tabs so PDF text is easier to read and compare.
    text = re.sub(r"[ \t]+", " ", text)
    # Keep paragraph breaks, but collapse very large blank gaps.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_tables_from_page(pdf_page: pymupdf.Page) -> list:
    # Type hint note: pdf_page is expected to be a PyMuPDF Page object.
    # Find tables on this page and convert each table into RAG-friendly text.
    # PyMuPDF docs: https://pymupdf.readthedocs.io/en/latest/page.html#Page.find_tables
    tables = []
    table_finder = pdf_page.find_tables()
    table_number = 1

    for table in table_finder.tables:
        rows = table.extract()
        tables.append({
            "title": f"Table {table_number}",
            "rows": rows,
            "text": table.to_markdown(),
            "extraction_method": "pymupdf_find_tables",
            "extraction_status": "success",
        })
        table_number = table_number + 1

    return tables


def is_image_present_on_page(pdf_page: pymupdf.Page) -> bool:
    # Type hint note: pdf_page is expected to be a PyMuPDF Page object.
    # Return True if this PDF page contains at least one embedded image.
    # PyMuPDF docs: https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_images
    return len(pdf_page.get_images(full=True)) > 0


def read_page_screenshot_with_vision(pdf_page: pymupdf.Page) -> str:
    # Type hint note: pdf_page is expected to be a PyMuPDF Page object.
    # Render the full PDF page as a screenshot.
    page_image = pdf_page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False).tobytes("png")
    page_image_base64 = base64.b64encode(page_image).decode("utf-8")

    # Send the full page screenshot to Vision and return only the extracted text.
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model=VISION_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract all readable text from this PDF page screenshot. Return only plain text.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{page_image_base64}",
                        "detail": "high",
                    },
                ],
            }
        ],
    )

    return clean_text(response.output_text)
