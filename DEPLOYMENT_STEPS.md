# Deployment Steps

Use this as the student checklist during Session 18.

## Part 1 - Understand The Flow

```text
Your laptop:
  code + requirements + .gitignore

GitHub:
  stores the code

Streamlit Community Cloud:
  reads code from GitHub and runs the app

Supabase:
  stores embeddings for RAG search

OpenAI:
  creates embeddings and answers questions
```

## Part 2 - Prepare Supabase

1. Open Supabase.
2. Open your project.
3. Go to SQL Editor.
4. Paste the content from `App/supabase_setup.sql`.
5. Click Run.

## Part 3 - Prepare Local Secrets

Create `App/.env`:

```text
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
SUPABASE_TABLE=documents
```

Do not commit `App/.env`.

## Part 4 - Test Locally

Run these commands from the repository root:

```powershell
pip install -r App/requirements.txt
streamlit run App/streamlit_app.py
```

Upload a PDF, click Train, then ask a question.

## Part 5 - Push To GitHub

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

Before pushing, run:

```powershell
git status
```

Check that `App/.env` is not listed.

## Part 6 - Deploy On Streamlit Community Cloud

1. Go to `https://share.streamlit.io`.
2. Sign in with GitHub.
3. Click Create app.
4. Choose your GitHub repository.
5. Set branch to `main`.
6. Set main file path to:

```text
App/streamlit_app.py
```

7. Open Advanced settings.
8. Paste secrets in TOML format:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your_supabase_service_role_key_here"
SUPABASE_TABLE = "documents"
```

9. Click Deploy.

## Common Deployment Errors

Missing package:

```text
ModuleNotFoundError
```

Fix: add the package to `App/requirements.txt`, commit, and push again.

Missing secret:

```text
Missing values: OPENAI_API_KEY
```

Fix: add secrets in Streamlit Advanced settings.

Wrong app path:

```text
File not found: streamlit_app.py
```

Fix: set main file path exactly to `App/streamlit_app.py`.

Supabase table missing:

```text
function match_documents does not exist
```

Fix: run `App/supabase_setup.sql` in Supabase SQL Editor.
