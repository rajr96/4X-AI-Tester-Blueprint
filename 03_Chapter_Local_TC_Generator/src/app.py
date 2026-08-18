"""Streamlit chat screen for Jira test-case generation."""

from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

from config_store import load_config
from jira_client import JiraError, fetch_issue
from llm_client import LLMError, generate


TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "test_case_template.md"
ISSUE_KEY_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b", re.IGNORECASE)


def _build_prompt(issue: dict[str, str]) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    for field, value in issue.items():
        template = template.replace(f"{{{{{field}}}}}", value)
    return template


def _issue_key(message: str) -> str | None:
    match = ISSUE_KEY_PATTERN.search(message)
    return match.group(1).upper() if match else None


def _render_message(message: dict[str, str]) -> None:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


st.set_page_config(page_title="Jira Test Case Generator", page_icon="🧪")
st.title("Jira Test Case Generator")
st.caption("Turn one Jira issue into a structured test-case draft.")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    _render_message(message)

if prompt := st.chat_input("Create test cases for QA-102"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    _render_message(st.session_state.messages[-1])
    key = _issue_key(prompt)
    if not key:
        answer = "Please include a Jira issue key, for example `QA-102`."
    else:
        config = load_config()
        try:
            if not config.has_jira_credentials:
                raise JiraError("Jira credentials are incomplete. Update the .env file.")
            with st.spinner(f"Fetching {key} and drafting test cases..."):
                issue = fetch_issue(config.jira_url, config.jira_email, config.jira_api_token, key)
                answer = generate(config, _build_prompt(issue))
        except (JiraError, LLMError, OSError) as exc:
            answer = str(exc)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    _render_message(st.session_state.messages[-1])