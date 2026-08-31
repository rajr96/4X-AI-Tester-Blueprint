import unittest
import json
from unittest.mock import patch

from src.jira_client import JiraClient
from src.llm_client import LLMClient
from src.plan_exporter import to_docx, to_pdf
from src.requirement_parser import RequirementParser
from src.test_plan_generator import TestPlan, TestPlanGenerator


class RequirementParserTests(unittest.TestCase):
    def test_extracts_functional_requirements_from_prd_description(self):
        description = """
h1. Product Requirements Document: VWO Login Dashboard

h2. Target Users

* Primary Users: Digital marketers, product managers, UX designers, and developers at growing businesses
* Secondary Users: Enterprise teams, conversion rate optimization specialists, and data analysts

h2. Business Objectives

* Ensure secure access to VWO's experimentation platform
* Minimize login friction to improve user adoption and retention

h2. Functional Requirements

h2. Authentication System

h2. Login Process

* Primary Authentication: Email and password-based login with secure validation
* Session Management: Secure session handling with configurable timeout periods
* Multi-Factor Authentication: Optional 2FA support for enhanced security

h2. User Input Validation

* Real-time Validation: Field validation on blur to provide immediate feedback
* Password Strength Indicators: Visual feedback for password requirements and strength
"""

        parser = RequirementParser()
        result = parser.parse({"key": "SCRUM-6", "fields": {"description": description}})

        self.assertIn("Primary Authentication: Email and password-based login with secure validation", result["acceptance_criteria"])
        self.assertIn("Session Management: Secure session handling with configurable timeout periods", result["acceptance_criteria"])
        self.assertNotIn("Primary Users: Digital marketers, product managers, UX designers, and developers at growing businesses", result["acceptance_criteria"])
        self.assertNotIn("Ensure secure access to VWO's experimentation platform", result["acceptance_criteria"])

    def test_extracts_requirements_from_mixed_markdown_and_atlassian_lists(self):
        description = """
# Login feature

## Target Users
- Customer support agents
- Admin users

## Functional Requirements

### Access Control
- Users must sign in with a valid email and password.
- Users who enter a wrong password see a clear error message.

### Password Recovery
1. The reset link must expire after 30 minutes.
2. The system must reject an email not associated with an account.

### Non-Functional Notes
- The page should feel modern and polished.
"""

        parser = RequirementParser()
        result = parser.parse({"key": "SCRUM-7", "fields": {"description": description}})

        self.assertIn("Users must sign in with a valid email and password.", result["acceptance_criteria"])
        self.assertIn("The reset link must expire after 30 minutes.", result["acceptance_criteria"])
        self.assertNotIn("The page should feel modern and polished.", result["acceptance_criteria"])

    def test_strips_jira_placeholder_tokens_from_requirements(self):
        description = """
h2. Functional Requirements

* Primary Authentication: Email and password-based login with secure validation{{56}}
* Session Management: Secure session handling with configurable timeout periods{{6}}
"""

        parser = RequirementParser()
        result = parser.parse({"key": "SCRUM-8", "fields": {"description": description}})

        self.assertIn("Primary Authentication: Email and password-based login with secure validation", result["acceptance_criteria"])
        self.assertIn("Session Management: Secure session handling with configurable timeout periods", result["acceptance_criteria"])
        self.assertNotIn("{{56}}", " ".join(result["acceptance_criteria"]))
        self.assertNotIn("{{6}}", " ".join(result["acceptance_criteria"]))


class TestPlanGeneratorTests(unittest.TestCase):
    def test_generates_cases_from_requirements(self):
        requirement = {
            "issue_key": "SCRUM-6",
            "summary": "VWO Login page requirement",
            "acceptance_criteria": [
                "Primary Authentication: Email and password-based login with secure validation",
                "Real-time Validation: Field validation on blur to provide immediate feedback",
                "Forgot Password Flow: Streamlined password reset process with secure token generation",
            ],
        }

        plan = TestPlanGenerator().generate(requirement)
        markdown = plan.to_markdown()

        self.assertGreater(len(plan.test_cases), 3)
        self.assertIn("Primary Authentication", markdown)
        self.assertIn("Real-time Validation", markdown)
        self.assertIn("Forgot Password Flow", markdown)
        self.assertIn("## Scope", markdown)
        self.assertIn("## Traceability", markdown)
        self.assertIn("## Risks", markdown)


class TestPlanExportTests(unittest.TestCase):
    def test_to_dict_and_json_export_are_available(self):
        requirement = {
            "issue_key": "SCRUM-6",
            "summary": "VWO Login page requirement",
            "acceptance_criteria": [
                "Primary Authentication: Email and password-based login with secure validation",
                "Real-time Validation: Field validation on blur to provide immediate feedback",
            ],
        }

        plan = TestPlanGenerator().generate(requirement)
        payload = plan.to_dict()

        self.assertEqual(payload["issue_key"], "SCRUM-6")
        self.assertIn("test_cases", payload)
        self.assertIn("Primary Authentication", plan.to_json())
        self.assertTrue(plan.to_json().startswith("{"))

    def test_to_html_export_is_available(self):
        requirement = {
            "issue_key": "SCRUM-6",
            "summary": "VWO Login page requirement",
            "acceptance_criteria": [
                "Primary Authentication: Email and password-based login with secure validation",
            ],
        }

        html = TestPlanGenerator().generate(requirement).to_html()

        self.assertIn("<html", html.lower())
        self.assertIn("Test Plan", html)
        self.assertIn("Primary Authentication", html)

    def test_word_and_pdf_exports_are_available(self):
        plan = TestPlanGenerator().generate({
            "issue_key": "SCRUM-6",
            "summary": "VWO Login page requirement",
            "acceptance_criteria": ["Primary Authentication: Email and password-based login with secure validation"],
        })

        self.assertTrue(to_docx(plan).startswith(b"PK"))
        self.assertTrue(to_pdf(plan).startswith(b"%PDF"))


class LocalGeneratorTests(unittest.TestCase):
    def test_local_text_generates_requirement_plan_without_jira(self):
        parser = RequirementParser()
        requirement = parser.parse_local_text("""
# Local Login Feature

## Functional Requirements

- Users must sign in with a valid email and password.
- A wrong password must show a clear error message.
- The system must allow password reset for registered users.
""")

        self.assertEqual(requirement["issue_key"], "LOCAL")
        self.assertIn("Users must sign in with a valid email and password.", requirement["acceptance_criteria"])

        plan = TestPlanGenerator().generate(requirement)
        self.assertGreater(len(plan.test_cases), 2)


class JiraClientTests(unittest.TestCase):
    def test_get_issue_uses_expected_auth_and_params(self):
        client = JiraClient("https://example.atlassian.net", "user@example.com", "token123")

        with patch("src.jira_client.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"key": "SCRUM-6"}
            mock_get.return_value.raise_for_status.return_value = None

            result = client.get_issue("SCRUM-6")

            self.assertEqual(result["key"], "SCRUM-6")
            mock_get.assert_called_once()

            called_args = mock_get.call_args
            self.assertIn("/rest/api/2/issue/SCRUM-6", called_args.args[0])
            self.assertIn("summary,description,status,priority,labels,assignee,project,issuetype,components,comment",
                          str(called_args.kwargs["params"]))

            headers = called_args.kwargs["headers"]
            self.assertIn("Authorization", headers)
            self.assertTrue(headers["Authorization"].startswith("Basic "))

    def test_get_issue_search_returns_expected_result(self):
        client = JiraClient("https://example.atlassian.net", "user@example.com", "token123")

        with patch("src.jira_client.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"issues": []}
            mock_get.return_value.raise_for_status.return_value = None

            data = client.get_issue_search("project = SCRUM")

            self.assertEqual(data["issues"], [])
            self.assertIn("/rest/api/2/search", mock_get.call_args.args[0])


class LLMClientTests(unittest.TestCase):
    @patch("src.llm_client.requests.post")
    def test_ollama_generation_uses_configured_model(self, mock_post):
        mock_post.return_value.raise_for_status.return_value = None
        mock_post.return_value.json.return_value = {
            "response": json.dumps({
                "objective": "Validate login behavior",
                "scope": ["Authentication flow"],
                "risks": ["Standard risk"]
            })
        }

        client = LLMClient(provider="ollama", ollama_url="http://localhost:11434", ollama_model="gemma3:1b")
        payload = client.generate("Create a summary for login requirements")

        self.assertEqual(payload["objective"], "Validate login behavior")
        self.assertIn("/api/generate", mock_post.call_args.args[0])
        self.assertEqual(mock_post.call_args.kwargs["json"]["model"], "gemma3:1b")

    @patch("src.llm_client.requests.post")
    def test_groq_generation_uses_api_token(self, mock_post):
        mock_post.return_value.raise_for_status.return_value = None
        mock_post.return_value.json.return_value = {
            "choices": [{
                "message": {"content": json.dumps({
                    "objective": "Validate login behavior",
                    "scope": ["Password reset"],
                    "risks": ["Token risk"]
                })}
            }]
        }

        client = LLMClient(provider="groq", groq_api_token="gsk_test", groq_model="openai/gpt-oss-20b")
        payload = client.generate("Create a summary for login requirements")

        self.assertEqual(payload["objective"], "Validate login behavior")
        self.assertIn("Authorization", mock_post.call_args.kwargs["headers"])
        self.assertEqual(mock_post.call_args.kwargs["json"]["model"], "openai/gpt-oss-20b")


if __name__ == "__main__":
    unittest.main()
