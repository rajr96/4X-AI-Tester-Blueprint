import argparse
import os
import sys

import requests
from dotenv import load_dotenv


load_dotenv()


def validate_connection(issue_key: str) -> dict:
    jira_base_url = os.getenv("JIRA_BASE_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_TOKEN")

    if not jira_base_url or not jira_email or not jira_token:
        raise ValueError("Missing JIRA_BASE_URL, JIRA_EMAIL, or JIRA_TOKEN in .env")

    url = f"{jira_base_url.rstrip('/')}/rest/api/2/issue/{issue_key}"
    auth = requests.auth.HTTPBasicAuth(jira_email, jira_token)
    response = requests.get(
        url,
        auth=auth,
        params={"fields": "summary,status,priority,issuetype,project"},
        timeout=30,
    )

    return {
        "status_code": response.status_code,
        "url": url,
        "ok": response.ok,
        "body": response.json() if response.content else {},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Jira connectivity and issue access.")
    parser.add_argument("--issue-id", required=True, help="Jira issue key to test, for example SCRUM-6")
    args = parser.parse_args()

    try:
        result = validate_connection(args.issue_id)
        print(f"Status: {result['status_code']}")
        print(f"URL: {result['url']}")
        print(f"OK: {result['ok']}")
        print(result['body'])
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
