import os
from typing import Any, Dict

import requests


class JiraClient:
    def __init__(self, jira_base_url: str, jira_email: str, jira_token: str):
        self.jira_base_url = jira_base_url.rstrip("/")
        self.jira_email = jira_email
        self.jira_token = jira_token

    def _headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {self._basic_auth_token()}",
        }

    def _basic_auth_token(self) -> str:
        import base64
        raw = f"{self.jira_email}:{self.jira_token}".encode("utf-8")
        return base64.b64encode(raw).decode("ascii")

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        url = f"{self.jira_base_url}/rest/api/2/issue/{issue_key}"
        params = {
            "fields": "summary,description,status,priority,labels,assignee,project,issuetype,components,comment"
        }
        response = requests.get(url, headers=self._headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_issue_search(self, jql: str) -> Dict[str, Any]:
        url = f"{self.jira_base_url}/rest/api/2/search"
        params = {"jql": jql, "fields": "summary,description,status,priority,labels,assignee,project,issuetype"}
        response = requests.get(url, headers=self._headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()
