from dotenv import load_dotenv
from pathlib import Path
import os


# Make paths stable locally and on Streamlit Community Cloud.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load local secrets from .env during development.
# In Streamlit Cloud, add these values in Advanced settings -> Secrets.
load_dotenv(PROJECT_ROOT / ".env")


def get_secret(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st

        return st.secrets.get(name, default)
    except Exception:
        return default

# Central values used throughout the lesson.
PDF_PATH = PROJECT_ROOT / "sample_pdf" / "SolarSmart_4_Page_Guide.pdf"
DOCUMENT_SOURCE = "solarsmart_4_page_guide"
DOCUMENT_TITLE = "SolarSmart Home Starter Guide"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
VISION_MODEL = get_secret("OPENAI_VISION_MODEL", CHAT_MODEL)

# External service settings.
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_SERVICE_ROLE_KEY")
TABLE_NAME = get_secret("SUPABASE_TABLE", "documents")

# Page titles are metadata labels. They do not control extraction.
PAGE_TITLES = {
    1: "Solar Readiness",
    2: "System Design",
    3: "Proposal Details",
    4: "Site Evidence",
}
