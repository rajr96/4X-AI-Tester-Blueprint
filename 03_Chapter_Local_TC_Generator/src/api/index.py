from __future__ import annotations

import re
import sys
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from config_store import load_config
from exporter import export_test_cases
from jira_client import JiraError, fetch_issue
from llm_client import LLMError, generate

app = FastAPI(title="Jira Test Case Generator")

TEMPLATE_PATH = project_root / "templates" / "test_case_template.md"
ISSUE_KEY_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b", re.IGNORECASE)


def _build_prompt(issue: dict[str, str]) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    for field, value in issue.items():
        template = template.replace(f"{{{{{field}}}}}", value)
    return template


def _issue_key(message: str) -> str | None:
    match = ISSUE_KEY_PATTERN.search(message)
    return match.group(1).upper() if match else None


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return """
    <!doctype html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <title>Jira Test Case Generator</title>
        <style>
          body { font-family: sans-serif; margin: 40px; background: #f8fafc; color: #0f172a; }
          .card { max-width: 720px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08); padding: 32px; }
          input, button { font: inherit; }
          input { width: 100%; padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 8px; margin-top: 8px; margin-bottom: 16px; }
          button { background: #2563eb; color: white; border: none; border-radius: 8px; padding: 10px 16px; cursor: pointer; }
          code { background: #f1f5f9; padding: 2px 6px; border-radius: 6px; }
        </style>
      </head>
      <body>
        <div class=\"card\">
          <h1>Jira Test Case Generator</h1>
          <p>This is the Vercel-hosted API wrapper for the Jira test-case generator.</p>
          <p>Example request payload:</p>
          <code>{"issue_key": "SCRUM-6"}</code>
          <form action=\"/api/generate\" method=\"post\" id=\"frm\">
            <label for=\"issue_key\">Issue key</label>
            <input id=\"issue_key\" name=\"issue_key\" value=\"SCRUM-6\" />
            <button type=\"submit\">Generate</button>
          </form>
        </div>
      </body>
    </html>
    """


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/generate")
async def generate_cases(request: Request) -> dict[str, str | list[str] | None]:
    payload: dict[str, str] = {}
    content_type = request.headers.get("content-type", "").lower()

    try:
        if "application/json" in content_type:
            payload = await request.json()
        elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
            form = await request.form()
            payload = {key: value for key, value in form.multi_items()}
        else:
            payload = dict(request.query_params)
    except Exception:
        payload = {}

    issue_key = (payload or {}).get("issue_key") or (payload or {}).get("issueKey")
    if not issue_key:
        raise HTTPException(status_code=400, detail="Issue key is required.")

    key = _issue_key(str(issue_key))
    if not key:
        raise HTTPException(status_code=400, detail="Please include a valid Jira issue key, for example SCRUM-6.")

    config = load_config()
    try:
        if not config.has_jira_credentials:
            raise JiraError("Jira credentials are incomplete. Update the .env file.")

        issue = fetch_issue(config.jira_url, config.jira_email, config.jira_api_token, key)
        response = generate(config, _build_prompt(issue))
        csv_path, xlsx_path = export_test_cases(key, response)
        return {
            "issue_key": key,
            "summary": issue.get("summary"),
            "csv_path": str(csv_path),
            "xlsx_path": str(xlsx_path),
            "status": "success",
        }
    except (JiraError, LLMError, OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
