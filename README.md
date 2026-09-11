# AI HR Recruitment Assistant — Minimal Run

This adds a minimal FastAPI backend and Streamlit frontend to test the local Ollama integration.

Requirements
 - Python 3.9+
 - Ollama installed locally

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run backend:

```powershell
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Run frontend:

```powershell
streamlit run frontend/app.py
```

If the Ollama CLI isn't on your PATH, set `OLLAMA_CLI_PATH` before running Python processes:

```powershell
$env:OLLAMA_CLI_PATH = 'C:\full\path\to\ollama.exe'
``` 
# AI HR Recruitment Assistant

Run `app.py` with Streamlit after installing dependencies.
