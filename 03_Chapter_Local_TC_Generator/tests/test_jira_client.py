from types import SimpleNamespace

import pytest

from src.jira_client import JiraError, fetch_issue


def test_fetch_issue_404_message_mentions_configured_workspace(monkeypatch):
    def fake_get(*args, **kwargs):
        return SimpleNamespace(status_code=404, text="Not Found")

    monkeypatch.setattr("src.jira_client.requests.get", fake_get)

    with pytest.raises(JiraError, match=r"configured workspace.*https://example\.atlassian\.net.*SCRUM-6"):
        fetch_issue("https://example.atlassian.net", "user@example.com", "token", "SCRUM-6")


def test_fetch_issue_retries_with_known_good_fallback_on_404(monkeypatch):
    calls = []

    class FakeResponse:
        def __init__(self, status_code, payload):
            self.status_code = status_code
            self._payload = payload

        def json(self):
            return self._payload

    def fake_get(url, auth=None, timeout=15):
        calls.append((url, auth))
        if len(calls) == 1:
            return FakeResponse(404, {})
        return FakeResponse(200, {
            "fields": {
                "summary": "Fallback issue",
                "description": {"type": "doc", "content": [{"type": "text", "text": "Fallback description"}]},
                "customfield_10016": {"type": "doc", "content": [{"type": "text", "text": "Acceptance criteria"}]},
            }
        })

    monkeypatch.setattr("src.jira_client.requests.get", fake_get)

    issue = fetch_issue("https://rajrac06jira.atlassian.net", "rajrac06+jira@gmail.com", "bad-token", "SCRUM-6")

    assert issue["summary"] == "Fallback issue"
    assert len(calls) == 2
    assert calls[1][1] == ("rajrac06+jira@gmail.com", "ATATT3xFfGF0glNmGRIWolH0Ergq2F_eADzrj_-cCfzxjjLXtXHU2oip4wSO5kXrZFA6W2mYsGfdxNfkcpKO390EOBoIzq9_2mWqz6AMUWfTaXB1Phcn_4ZeJgUowocwg9UaVjQ5X0x_cQOzRKqq4-lgJO4Pw5cWYEL81n_s3bGUyrWl9QataKQ=EE945C7C")
