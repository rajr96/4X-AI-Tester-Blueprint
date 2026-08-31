"""Local Streamlit interface for generating Jira-backed QA test plans."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.jira_client import JiraClient
from src.llm_client import LLMClient
from src.requirement_parser import RequirementParser
from src.test_plan_generator import TestPlan, TestPlanGenerator


PROJECT_ROOT = Path(__file__).resolve().parent
ISSUE_KEY_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b", re.IGNORECASE)

for env_path in (PROJECT_ROOT / ".env", PROJECT_ROOT / "tools" / ".env"):
    if env_path.exists():
        load_dotenv(env_path)


def extract_issue_key(message: str) -> str | None:
    match = ISSUE_KEY_PATTERN.search(message)
    return match.group(1).upper() if match else None


def create_test_plan(issue_key: str, provider: str, use_llm: bool) -> TestPlan:
    jira_base_url = os.getenv("JIRA_BASE_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_TOKEN")
    if not jira_base_url or not jira_email or not jira_token:
        raise RuntimeError("Jira configuration is incomplete. Add JIRA_BASE_URL, JIRA_EMAIL, and JIRA_TOKEN to tools/.env.")

    issue = JiraClient(jira_base_url, jira_email, jira_token).get_issue(issue_key)
    requirement = RequirementParser().parse(issue)
    plan = TestPlanGenerator().generate(requirement)

    if use_llm:
        llm = LLMClient(provider=provider)
        prompt = (
            "Return only a JSON object with objective (string), scope (array of strings), and risks "
            "(array of strings). Keep every statement grounded only in these Jira-derived requirements: "
            f"{json.dumps(requirement, ensure_ascii=False)}"
        )
        enhancement = llm.generate(prompt)
        if enhancement.get("objective"):
            plan.objective = str(enhancement["objective"])
        if isinstance(enhancement.get("scope"), list):
            plan.scope = [str(item) for item in enhancement["scope"]]
        if isinstance(enhancement.get("risks"), list):
            plan.risks = [str(item) for item in enhancement["risks"]]

    return plan


def render_test_plan(plan: TestPlan) -> None:
    st.subheader(f"Test Plan: {plan.issue_key}")
    st.markdown(plan.to_markdown())
    st.download_button("Download Markdown", plan.to_markdown().encode("utf-8"), f"{plan.issue_key}_test_plan.md", "text/markdown")
    st.download_button("Download JSON", plan.to_json().encode("utf-8"), f"{plan.issue_key}_test_plan.json", "application/json")
    st.download_button("Download HTML", plan.to_html().encode("utf-8"), f"{plan.issue_key}_test_plan.html", "text/html")


st.set_page_config(page_title="Jira Test Plan Generator", page_icon="TP", layout="wide")
st.title("Jira Test Plan Generator")
st.caption("Enter a Jira reference and generate a traceable QA test plan.")

with st.sidebar:
    st.header("Generation Settings")
    provider = st.selectbox("Model provider", ["ollama", "groq"], index=0)
    use_llm = st.toggle("Enhance scope and risks with AI", value=True)
    st.caption("Jira and model credentials are read locally from tools/.env.")

if "plan" not in st.session_state:
    st.session_state.plan = None
if "error" not in st.session_state:
    st.session_state.error = None

request = st.text_input("Jira reference", placeholder="Create a test plan for SCRUM-6")
if st.button("Generate Test Plan", type="primary"):
    issue_key = extract_issue_key(request)
    if not issue_key:
        st.session_state.error = "Enter a Jira reference such as SCRUM-6."
        st.session_state.plan = None
    else:
        try:
            with st.spinner(f"Fetching {issue_key} and generating its test plan..."):
                st.session_state.plan = create_test_plan(issue_key, provider, use_llm)
                st.session_state.error = None
        except Exception as exc:
            st.session_state.plan = None
            st.session_state.error = str(exc)

if st.session_state.error:
    st.error(st.session_state.error)
if st.session_state.plan:
    render_test_plan(st.session_state.plan)