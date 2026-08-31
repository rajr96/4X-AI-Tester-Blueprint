import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from src.jira_client import JiraClient
from src.llm_client import LLMClient
from src.requirement_parser import RequirementParser
from src.test_plan_generator import TestPlanGenerator


project_root = Path(__file__).resolve().parent
for env_path in (project_root / ".env", project_root / "tools" / ".env"):
    if env_path.exists():
        load_dotenv(env_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a test plan from a Jira issue ID or local requirement text.")
    parser.add_argument("--issue-id", help="Jira issue key like SCRUM-6")
    parser.add_argument("--output", default="output/test-plan.md", help="Output path for generated test plan")
    parser.add_argument("--json-output", default=None, help="Optional JSON export path for the generated test plan")
    parser.add_argument("--html-output", default=None, help="Optional HTML export path for the generated test plan")
    parser.add_argument("--local-text", default=None, help="Plain-text requirement document for local generation")
    parser.add_argument("--summary", default="Local requirement", help="Summary used when generating locally")
    parser.add_argument("--provider", choices=["ollama", "groq"], default=None,
                        help="Optional model provider override: ollama or groq")
    parser.add_argument("--use-llm", action="store_true", help="Attempt to enhance the plan with the configured Ollama/Groq model.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    parser = RequirementParser()

    if args.local_text:
        requirement = parser.parse_local_text(args.local_text, summary=args.summary)
    else:
        if not args.issue_id:
            raise ValueError("Provide either --issue-id or --local-text")

        jira_base_url = os.getenv("JIRA_BASE_URL")
        jira_email = os.getenv("JIRA_EMAIL")
        jira_token = os.getenv("JIRA_TOKEN")

        if not jira_base_url or not jira_email or not jira_token:
            raise ValueError("Missing JIRA_BASE_URL, JIRA_EMAIL, or JIRA_TOKEN in .env")

        jira_client = JiraClient(jira_base_url=jira_base_url, jira_email=jira_email, jira_token=jira_token)
        issue = jira_client.get_issue(args.issue_id)
        requirement = parser.parse(issue)

    generator = TestPlanGenerator()
    test_plan = generator.generate(requirement)

    llm_provider = args.provider or os.getenv("LLM_PROVIDER")
    if args.use_llm or llm_provider in {"ollama", "groq"} or os.getenv("OLLAMA_MODEL") or os.getenv("GROQ_API_TOKEN"):
        try:
            llm = LLMClient(provider=llm_provider, ollama_url=os.getenv("OLLAMA_URL"),
                            ollama_model=os.getenv("OLLAMA_MODEL"),
                            groq_api_token=os.getenv("GROQ_API_TOKEN") or os.getenv("GROQ_API_KEY"),
                            groq_model=os.getenv("GROQ_MODEL"))
            prompt = (
                "Return only valid JSON with keys: objective, scope, risks. "
                "Based on this requirement set, create a concise QA objective, a scope list, and risk list. "
                f"Requirements: {json.dumps(requirement, ensure_ascii=False)}"
            )
            llm_payload = llm.generate(prompt)

            if isinstance(llm_payload, dict):
                if llm_payload.get("objective"):
                    test_plan.objective = str(llm_payload["objective"])
                if isinstance(llm_payload.get("scope"), list):
                    test_plan.scope = [str(item) for item in llm_payload["scope"]]
                if isinstance(llm_payload.get("risks"), list):
                    test_plan.risks = [str(item) for item in llm_payload["risks"]]
        except Exception:
            pass

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(test_plan.to_markdown(), encoding="utf-8")

    json_output_path = None
    if args.json_output:
        json_output_path = Path(args.json_output)
        json_output_path.parent.mkdir(parents=True, exist_ok=True)
        json_output_path.write_text(test_plan.to_json(), encoding="utf-8")

    html_output_path = None
    if args.html_output:
        html_output_path = Path(args.html_output)
        html_output_path.parent.mkdir(parents=True, exist_ok=True)
        html_output_path.write_text(test_plan.to_html(), encoding="utf-8")

    print(json.dumps({
        "issue_key": requirement["issue_key"],
        "summary": requirement["summary"],
        "output": str(output_path),
        "json_output": str(json_output_path) if json_output_path else None,
        "html_output": str(html_output_path) if html_output_path else None,
        "mode": "local" if args.local_text else "jira",
    }, indent=2))


if __name__ == "__main__":
    main()
