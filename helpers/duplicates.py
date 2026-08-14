import re

from helpers.pdf_helpers import clean_text


def print_inventory_character_counts(title: str, page_inventory: list) -> None:
    # Show the plain text size for every page before and after dedupe.
    print("\n" + title)

    for page in page_inventory:
        print(
            "Page", page["page_number"],
            "raw_text_chars=", len(page["raw_text"]),
            "processed_text_chars=", len(page["processed_text"]),
            "tables=", len(page["tables"]),
            "image_found=", page["image_found"],
            "image_text_chars=", len(page["image_text"]),
        )


def remove_duplicate_text_from_inventory(page_inventory: list) -> list:
    # Dedupe runs after every page has text, tables, and image_text.
    # For the beginner version, we only remove table cell lines from raw_text.
    for page in page_inventory:
        duplicate_lines = set()

        for table in page["tables"]:
            for row in table.get("rows", []):
                for cell in row:
                    if cell is not None:
                        line_key = re.sub(r"\s+", " ", str(cell).strip()).casefold()
                        if line_key:
                            duplicate_lines.add(line_key)

        kept_lines = []
        removed_count = 0

        for line in page["raw_text"].splitlines():
            line_key = re.sub(r"\s+", " ", line.strip()).casefold()

            if line_key and line_key in duplicate_lines:
                removed_count = removed_count + 1
            else:
                kept_lines.append(line)

        page["processed_text"] = clean_text("\n".join(kept_lines))
        page["duplicate_text_lines_removed"] = removed_count

    return page_inventory
