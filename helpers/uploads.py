from pathlib import Path
import re

from helpers.settings import PROJECT_ROOT


UPLOAD_DIR = PROJECT_ROOT / "uploads"


def save_uploaded_pdf(uploaded_file) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", uploaded_file.name)
    pdf_path = UPLOAD_DIR / safe_name

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path.write_bytes(uploaded_file.getbuffer())

    return pdf_path
