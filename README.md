# 4X AI Tester Blueprint

## go go go
Use this command prompt to perform the full git workflow:

```text
go go go:
1. Update parent README file.
2. Add all files.
3. Commit all changes.
4. Push code to https://github.com/rajr96/4X-AI-Tester-Blueprint.git
```

## Repository Structure
- 01_chapter_LLM_Basics
- 02_Chapter_Prompt_eng
- 03_Chapter_Local_TC_Generator
- 04_Chapter_JobKitAI
- References

## Verified Working Apps

### 1) JobTracker (Vite + React)
- Local URL: http://localhost:4173/
- Vercel production URL: https://jobtrackerai-five.vercel.app
- Project folder: `05_Chapter_JobTrackerAI`

Start locally:
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\05_Chapter_JobTrackerAI"
npm run dev -- --host 0.0.0.0 --port 4173
```

### 2) Jira Test Case Generator (FastAPI + Vercel)
- Local URL: http://localhost:8501/ (Streamlit dev mode)
- Vercel production URL: https://jira-test-case-generator-delta.vercel.app
- Project folder: `03_Chapter_Local_TC_Generator`

Start locally for API validation:
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\03_Chapter_Local_TC_Generator"
python -m uvicorn api.index:app --host 0.0.0.0 --port 8000
```

Use `python -m streamlit run src/app.py` only for the original local Streamlit UI if needed.

The `03_Chapter_Local_TC_Generator/src` folder contains a Streamlit application that fetches a Jira issue, loads a local test-case template, generates test cases with Ollama, and falls back to Groq when configured and required.

### Files

- `app.py` - Chat screen and Jira-to-test-case workflow.
- `pages/settings.py` - Provider selection and configuration status screen.
- `config_store.py` - Loads local `.env` values and persists the non-secret provider setting.
- `jira_client.py` - Fetches and normalizes Jira issue details.
- `llm_client.py` - Calls Ollama by default with temperature 0, strict JSON validation, and Groq fallback.
- `exporter.py` - Validates generated rows and exports CSV/Excel files with timestamped names.
- `templates/test_case_template.md` - Test-case generation prompt template.
- `requirements.txt` - Python dependencies for Streamlit, Jira, LLM, and CSV/Excel export.
- `plan.md` - Approved implementation plan.
- `.env.example` - Safe environment-variable template.
- `Results/` - Generated timestamped CSV and Excel test-case reports.

### Configuration

Copy `.env.example` to `.env` and provide Jira credentials locally. The `.env` file is ignored by Git and must never be committed. The default local model is Ollama `gemma3:1b` at `http://localhost:11434`; no model download is performed by the app.

### Run

```powershell
cd 03_Chapter_Local_TC_Generator/src
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Use the Chat screen with a request such as `create test cases for SCRUM-6`. Select the LLM provider from the Settings screen. Generated reports are saved under `src/Results` with names such as `SCRUM-6_test_cases_20260819_002146.csv` and `.xlsx`. Each applicable scenario produces 2 to 5 cases, with 2 to 70 cases allowed overall; invalid model responses are rejected before export.

- Last synchronized: 2026-08-19
