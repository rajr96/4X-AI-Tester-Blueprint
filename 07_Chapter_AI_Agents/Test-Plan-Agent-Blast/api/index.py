"""Vercel entry point for the Jira Test Plan Generator."""

from __future__ import annotations

import base64
import json
import os
import re
import sys
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.jira_client import JiraClient
from src.llm_client import LLMClient
from src.plan_exporter import to_docx, to_pdf
from src.requirement_parser import RequirementParser
from src.test_plan_generator import TestPlan, TestPlanGenerator


app = FastAPI(title="Jira Test Plan Generator")
ISSUE_KEY_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b", re.IGNORECASE)


def extract_issue_key(value: str) -> str | None:
    match = ISSUE_KEY_PATTERN.search(value)
    return match.group(1).upper() if match else None


def build_plan(issue_key: str, use_llm: bool) -> TestPlan:
    jira_base_url = os.getenv("JIRA_BASE_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_TOKEN")
    if not jira_base_url or not jira_email or not jira_token:
        raise RuntimeError("Jira configuration is incomplete on the deployment.")

    issue = JiraClient(jira_base_url, jira_email, jira_token).get_issue(issue_key)
    requirement = RequirementParser().parse(issue)
    plan = TestPlanGenerator().generate(requirement)

    if use_llm:
        prompt = (
            "Return only a JSON object with objective (string), scope (array of strings), and risks "
            "(array of strings). Keep every statement grounded only in these Jira-derived requirements: "
            f"{json.dumps(requirement, ensure_ascii=False)}"
        )
        try:
            enhancement = LLMClient(provider="groq").generate(prompt)
            if enhancement.get("objective"):
                plan.objective = str(enhancement["objective"])
            if isinstance(enhancement.get("scope"), list):
                plan.scope = [str(item) for item in enhancement["scope"]]
            if isinstance(enhancement.get("risks"), list):
                plan.risks = [str(item) for item in enhancement["risks"]]
        except (requests.RequestException, RuntimeError, ValueError):
            pass

    return plan


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jira Test Plan Generator</title>
<style>
  :root { --ink:#172033; --paper:#f5f7f4; --accent:#087f5b; --line:#cdd8d4; }
  * { box-sizing:border-box; } body { margin:0; color:var(--ink); background:var(--paper); font-family:Georgia, serif; }
  main { width:min(900px, calc(100% - 32px)); margin:10vh auto; } h1 { font-size:clamp(2rem, 5vw, 3.5rem); margin:0 0 8px; letter-spacing:0; }
  p { font-family:Verdana, sans-serif; line-height:1.6; } form { display:flex; gap:10px; margin-top:32px; } input { flex:1; min-width:0; padding:14px; border:1px solid var(--line); border-radius:5px; font:16px Verdana, sans-serif; }
  button { padding:14px 20px; border:0; border-radius:5px; background:var(--accent); color:white; font:600 15px Verdana, sans-serif; cursor:pointer; }
    .settings { display:flex; justify-content:flex-end; margin-top:14px; } .toggle { display:inline-flex; align-items:center; gap:9px; font:14px Verdana,sans-serif; cursor:pointer; } .toggle input { appearance:none; width:38px; height:22px; margin:0; padding:0; border:0; border-radius:11px; background:#9ca3af; position:relative; cursor:pointer; } .toggle input::after { content:""; position:absolute; width:16px; height:16px; top:3px; left:3px; border-radius:50%; background:white; transition:transform .15s ease; } .toggle input:checked { background:var(--accent); } .toggle input:checked::after { transform:translateX(16px); } #result { margin-top:32px; } .error { color:#b42318; font-family:Verdana,sans-serif; } .downloads { display:flex; flex-wrap:wrap; gap:10px; margin-top:16px; } .downloads button { background:#172033; padding:10px 14px; }
  @media (max-width:600px) { main { margin:48px auto; } form { flex-direction:column; } button { width:100%; } }
</style></head><body><main>
<h1>Jira Test Plan Generator</h1><p>Enter a Jira reference to generate a downloadable, traceable QA test plan.</p>
<form id="generator"><input name="issue_key" placeholder="SCRUM-6" required><button type="submit">Generate Plan</button></form>
<div class="settings"><label class="toggle"><input type="checkbox" id="use_llm" checked><span>Enhance scope and risks with Groq</span></label></div><div id="result"></div>
<script>
const form=document.querySelector('#generator'), result=document.querySelector('#result');
form.addEventListener('submit', async event => { event.preventDefault(); result.textContent='Generating test plan...';
  const key=new FormData(form).get('issue_key'); const response=await fetch('/api/generate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({issue_key:key, use_llm:document.querySelector('#use_llm').checked})});
  const data=await response.json(); if(!response.ok) { result.innerHTML='<p class="error">'+data.detail+'</p>'; return; }
    result.innerHTML='<p>Plan for <strong>'+data.issue_key+'</strong> is ready.</p><div class="downloads"><button data-format="html">HTML</button><button data-format="markdown">Markdown</button><button data-format="json">JSON</button><button data-format="docx">Word</button><button data-format="pdf">PDF</button></div>';
    result.querySelectorAll('button').forEach(button => button.addEventListener('click', () => download(button.dataset.format, data, data.issue_key)));
});
function download(format, data, key) { const textFormats={html:'text/html',markdown:'text/markdown',json:'application/json'}; let blob, extension;
    if(textFormats[format]) { blob=new Blob([data[format]], {type:textFormats[format]}); extension=format === 'markdown' ? 'md' : format; }
    else { const bytes=Uint8Array.from(atob(data[format]), char => char.charCodeAt(0)); blob=new Blob([bytes], {type:format === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}); extension=format; }
    const link=document.createElement('a'); link.href=URL.createObjectURL(blob); link.download=key+'_test_plan.'+extension; link.click(); URL.revokeObjectURL(link.href); }
</script></main></body></html>"""


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/generate")
async def generate(request: Request) -> dict[str, str]:
    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="The request must contain JSON.") from exc

    issue_key = extract_issue_key(str(payload.get("issue_key", "")))
    if not issue_key:
        raise HTTPException(status_code=400, detail="Enter a Jira reference such as SCRUM-6.")

    try:
        plan = build_plan(issue_key, bool(payload.get("use_llm", True)))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "issue_key": issue_key,
        "markdown": plan.to_markdown(),
        "json": plan.to_json(),
        "html": plan.to_html(),
        "docx": base64.b64encode(to_docx(plan)).decode("ascii"),
        "pdf": base64.b64encode(to_pdf(plan)).decode("ascii"),
    }