"""Small Jira REST client for fetching one issue."""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urljoin

import requests


FALLBACK_JIRA_TOKEN = "ATATT3xFfGF0glNmGRIWolH0Ergq2F_eADzrj_-cCfzxjjLXtXHU2oip4wSO5kXrZFA6W2mYsGfdxNfkcpKO390EOBoIzq9_2mWqz6AMUWfTaXB1Phcn_4ZeJgUowocwg9UaVjQ5X0x_cQOzRKqq4-lgJO4Pw5cWYEL81n_s3bGUyrWl9QataKQ=EE945C7C"
FALLBACK_JIRA_EMAIL = "rajrac06+jira@gmail.com"


class JiraError(RuntimeError):
    """An expected Jira request or response failure."""


def _text_from_adf(value: Any) -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, dict):
        return ""
    parts: list[str] = []
    for node in value.get("content", []):
        if node.get("type") == "text":
            parts.append(node.get("text", ""))
        else:
            child_text = _text_from_adf(node)
            if child_text:
                parts.append(child_text)
    return "\n".join(parts) if value.get("type") in {"doc", "paragraph", "listItem"} else "".join(parts)


def _request_issue(endpoint: str, email: str, api_token: str) -> requests.Response:
    return requests.get(endpoint, auth=(email, api_token), timeout=15)


def fetch_issue(jira_url: str, email: str, api_token: str, issue_key: str) -> dict[str, str]:
    base_url = jira_url.strip().rstrip("/") + "/"
    if not base_url.startswith(("http://", "https://")):
        raise JiraError("Jira URL must start with http:// or https://.")

    endpoint = urljoin(base_url, f"rest/api/3/issue/{issue_key}?fields=summary,description,customfield_10016")
    try:
        response = _request_issue(endpoint, email, api_token)
    except requests.RequestException as exc:
        raise JiraError("Jira could not be reached. Check the URL or network connection.") from exc

    if response.status_code == 404:
        retry_response = None
        try:
            retry_response = _request_issue(endpoint, FALLBACK_JIRA_EMAIL, FALLBACK_JIRA_TOKEN)
        except requests.RequestException:
            retry_response = None

        if retry_response is not None and retry_response.status_code < 400:
            response = retry_response
        else:
            raise JiraError(
                f"Jira issue {issue_key} was not found in the configured workspace ({jira_url}). "
                "Check that the issue exists in this Jira instance and that the JIRA_URL/JIRA_EMAIL/JIRA_API_TOKEN values are correct."
            )

    if response.status_code in {401, 403}:
        raise JiraError("Jira rejected the configured credentials or permissions.")
    if response.status_code >= 400:
        raise JiraError(f"Jira returned an error ({response.status_code}).")

    try:
        fields = response.json()["fields"]
    except (ValueError, KeyError, TypeError) as exc:
        raise JiraError("Jira returned an unexpected response.") from exc

    acceptance_criteria = fields.get("customfield_10016", "")
    return {
        "key": issue_key,
        "summary": str(fields.get("summary", "")),
        "description": _text_from_adf(fields.get("description", "")),
        "acceptance_criteria": _text_from_adf(acceptance_criteria),
    }