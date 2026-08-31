import json
from typing import Dict, List


class TestCase:
    def __init__(self, test_id: str, title: str, category: str, steps: List[str], expected_result: str):
        self.test_id = test_id
        self.title = title
        self.category = category
        self.steps = steps
        self.expected_result = expected_result

    def to_dict(self) -> Dict[str, str | List[str]]:
        return {
            "id": self.test_id,
            "title": self.title,
            "category": self.category,
            "steps": self.steps,
            "expected_result": self.expected_result,
        }


class TestPlan:
    def __init__(self, issue_key: str, summary: str, objective: str, test_cases: List[TestCase], scope: List[str] | None = None, risks: List[str] | None = None):
        self.issue_key = issue_key
        self.summary = summary
        self.objective = objective
        self.test_cases = test_cases
        self.scope = scope or ["Authentication flow", "Validation behavior", "Password recovery", "User experience and responsiveness"]
        self.risks = risks or [
            "Unclear acceptance criteria may require product clarification.",
            "Authentication flows can be sensitive to session and browser state.",
            "Recovery flows may depend on email delivery or tenant configuration."
        ]

    def to_markdown(self) -> str:
        lines = [
            f"# Test Plan: {self.issue_key}",
            "",
            f"**Summary:** {self.summary}",
            f"**Objective:** {self.objective}",
            "",
            "## Scope",
            "",
            *[f"- {item}" for item in self.scope],
            "",
            "## Assumptions",
            "",
            "- Jira issue is the source of truth for product requirements.",
            "- Only valid, requirement-backed behavior will be tested.",
            "- Missing business details will be reported rather than assumed.",
            "",
            "## Risks",
            "",
            *[f"- {item}" for item in self.risks],
            "",
            "## Traceability",
            "",
            "- Source: Jira issue and associated requirement bullets.",
            "- Coverage areas: login, validation, session handling, password recovery, and user input scenarios.",
            "",
            "## Test Cases",
            "",
        ]

        for case in self.test_cases:
            lines.append(f"### {case.test_id}: {case.title}")
            lines.append(f"**Category:** {case.category}")
            lines.append("**Steps:**")
            for step in case.steps:
                lines.append(f"- {step}")
            lines.append(f"**Expected Result:** {case.expected_result}")
            lines.append("")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, object]:
        return {
            "issue_key": self.issue_key,
            "summary": self.summary,
            "objective": self.objective,
            "scope": self.scope,
            "risks": self.risks,
            "test_cases": [case.to_dict() for case in self.test_cases],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def to_html(self) -> str:
        rows = "".join(
            f"<tr><td>{case.test_id}</td><td>{case.title}</td><td>{case.category}</td><td><ul>{''.join(f'<li>{step}</li>' for step in case.steps)}</ul></td><td>{case.expected_result}</td></tr>"
            for case in self.test_cases
        )

        assumption_html = "".join(f"<li>{item}</li>" for item in [
            "Jira issue is the source of truth for product requirements.",
            "Only valid, requirement-backed behavior will be tested.",
            "Missing business details will be reported rather than assumed.",
        ])

        return f"""<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Test Plan: {self.issue_key}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #1f2937; }}
    h1, h2 {{ color: #111827; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #f3f4f6; }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin-bottom: 4px; }}
  </style>
</head>
<body>
  <h1>Test Plan: {self.issue_key}</h1>
  <p><strong>Summary:</strong> {self.summary}</p>
  <p><strong>Objective:</strong> {self.objective}</p>

  <h2>Scope</h2>
  <ul>{''.join(f'<li>{item}</li>' for item in self.scope)}</ul>

  <h2>Assumptions</h2>
  <ul>{assumption_html}</ul>

  <h2>Risks</h2>
  <ul>{''.join(f'<li>{item}</li>' for item in self.risks)}</ul>

  <h2>Test Cases</h2>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Category</th>
        <th>Steps</th>
        <th>Expected Result</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</body>
</html>"""


class TestPlanGenerator:
    def generate(self, requirement: Dict[str, str | List[str]]) -> TestPlan:
        issue_key = requirement.get("issue_key", "UNKNOWN")
        summary = requirement.get("summary", "")
        objective = f"Validate the behavior for {summary}"

        criteria = requirement.get("acceptance_criteria", [])
        if not isinstance(criteria, list):
            criteria = [str(criteria)]

        if criteria:
            test_cases = []
            for index, criterion in enumerate(criteria[:6], start=1):
                title = self._title_from_criterion(criterion)
                category = self._category_from_criterion(criterion)
                steps = self._steps_from_criterion(criterion)
                expected_result = f"The feature behavior is validated against: {criterion}"

                test_cases.append(
                    TestCase(
                        f"TC-{index:02d}",
                        title,
                        category,
                        steps,
                        expected_result,
                    )
                )

            # Add explicit negative and boundary coverage for realistic QA planning.
            test_cases.append(
                TestCase(
                    "TC-NEG-01",
                    "Invalid input handling",
                    "Negative",
                    [
                        "Attempt the flow with invalid or missing data",
                        "Trigger the action or submit the form",
                        "Check that the system blocks the action and surfaces a clear message",
                    ],
                    "The system rejects invalid input and provides actionable feedback without breaking the flow.",
                )
            )
            test_cases.append(
                TestCase(
                    "TC-BND-01",
                    "Boundary and edge conditions",
                    "Boundary",
                    [
                        "Exercise the smallest and largest valid inputs",
                        "Repeat the scenario with edge-case values",
                        "Confirm the system remains stable and consistent",
                    ],
                    "The login or validation flow remains stable across valid boundary values and edge conditions.",
                )
            )

            if not test_cases:
                test_cases = [
                    TestCase(
                        "TC-01",
                        "Happy path validation",
                        "Positive",
                        [
                            "Open the relevant feature or page",
                            "Provide valid input based on the issue requirements",
                            "Submit or trigger the action",
                        ],
                        "The system behaves as expected and succeeds without error.",
                    )
                ]
        else:
            test_cases = [
                TestCase(
                    "TC-01",
                    "Happy path validation",
                    "Positive",
                    [
                        "Open the relevant feature or page",
                        "Provide valid input based on the issue requirements",
                        "Submit or trigger the action",
                    ],
                    "The system behaves as expected and succeeds without error.",
                )
            ]

        return TestPlan(issue_key, summary, objective, test_cases)

    def _title_from_criterion(self, criterion: str) -> str:
        if ":" in criterion:
            return criterion.split(":", 1)[0].strip()
        return criterion[:60].strip()

    def _category_from_criterion(self, criterion: str) -> str:
        lower = criterion.lower()
        if "error" in lower or "invalid" in lower or "negative" in lower:
            return "Negative"
        if "validation" in lower or "password" in lower or "email" in lower or "reset" in lower:
            return "Validation"
        if "session" in lower or "authentication" in lower or "login" in lower:
            return "Positive"
        return "Functional"

    def _steps_from_criterion(self, criterion: str) -> List[str]:
        prefix = criterion.split(":", 1)[0].strip() if ":" in criterion else "Requirement validation"
        return [
            f"Open the relevant screen or flow for {prefix}",
            "Enter valid data consistent with the requirement",
            "Trigger the action and observe the result",
            "Verify the output matches the requirement wording",
        ]
