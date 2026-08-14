# Session 18 - Deploy a Streamlit RAG App

In this session, we package the multi-page PDF RAG app and deploy it online.

The goal is not to learn every Git command. The goal is to understand the minimum workflow needed to share a real AI app:

```text
local folder -> Git -> GitHub -> Streamlit Community Cloud -> live app URL
```

## What This App Does

1. Upload a PDF.
2. Extract text, tables, and image text.
3. Split the extracted content into chunks.
4. Create OpenAI embeddings.
5. Store the chunks in Supabase.
6. Ask questions using RAG.

## Why GitHub And Streamlit Cloud?

GitHub stores and versions our code.

Streamlit Community Cloud runs our Python Streamlit app online. GitHub Pages is not enough for this project because Streamlit apps need a Python server.

## Folder Structure

```text
Session_18/
  .gitignore
  App/
    streamlit_app.py
    requirements.txt
    README.md
    DEPLOYMENT_STEPS.md
    supabase_setup.sql
    .env                  # local only, never committed
    .streamlit/
      secrets.example.toml
    helpers/
    sample_pdf/
```

## Local Setup

Run these commands from the repository root.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r App/requirements.txt
```

Create a local `App/.env` file:

```text
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
SUPABASE_TABLE=documents
```

Run `App/supabase_setup.sql` once in Supabase SQL Editor.

Start the app:

```powershell
streamlit run App/streamlit_app.py
```

## GitHub Commands

Run these commands from the repository root:

```powershell
git init
git status
git add .
git commit -m "Deploy Streamlit RAG app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Important Security Rule

Never push `App/.env` or real API keys to GitHub.

This project includes:

```text
App/.streamlit/secrets.example.toml
```

This file shows the format only. It does not contain real secrets.
