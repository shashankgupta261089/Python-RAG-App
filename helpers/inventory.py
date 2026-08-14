from pathlib import Path
import pymupdf

from helpers.pdf_helpers import (
    clean_text,
    extract_tables_from_page,
    is_image_present_on_page,
    read_page_screenshot_with_vision,
)
from helpers.settings import PAGE_TITLES


def build_page_record(pdf: pymupdf.Document, pdf_page: pymupdf.Page, page_number: int) -> dict:
    # Type hint note: pdf_page is one PyMuPDF Page from the PDF loop.
    # Start with a blank page record.
    page_record = {
        "page_number": page_number,
        "title": PAGE_TITLES.get(page_number, f"Page {page_number}"),
        "text_found": False,
        "table_found": False,
        "image_found": False,
        "table_detection_error": "",
        "raw_text": "",
        "processed_text": "",
        "tables": [],
        "image_text": "",
        "duplicate_text_lines_removed": 0,
    }

    # 1. Check and add normal selectable text.
    page_text = clean_text(pdf_page.get_text("text"))
    page_record["raw_text"] = page_text
    page_record["processed_text"] = page_text
    page_record["text_found"] = bool(page_text)

    # 2. Check and add tables using one PyMuPDF table function.
    try:
        page_record["tables"] = extract_tables_from_page(pdf_page)
        page_record["table_found"] = len(page_record["tables"]) > 0
    except Exception as error:
        page_record["table_detection_error"] = str(error)

    # 3. Check and add page screenshot Vision text only if this page has images.
    page_record["image_found"] = is_image_present_on_page(pdf_page)

    if page_record["image_found"]:
        page_record["image_text"] = read_page_screenshot_with_vision(pdf_page)

    return page_record


def build_page_inventory(pdf_path: str | Path) -> list:
    # Start blank, then append one completed page record at a time.
    inventory = []

    with pymupdf.open(pdf_path) as pdf:
        page_number = 1

        for pdf_page in pdf:
            page_record = build_page_record(pdf, pdf_page, page_number)
            inventory.append(page_record)
            page_number = page_number + 1

    return inventory
