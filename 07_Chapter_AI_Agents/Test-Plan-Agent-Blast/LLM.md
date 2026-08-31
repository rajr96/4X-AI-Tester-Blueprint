# LLM Project Constitution: Jira Test Plan Generator

## Objective
This file defines the project constitution for the Jira test-plan creator. It captures the schema, behavioral rules, and architecture that guide the tool when working with a Jira issue ID.

## Core Principle
The LLM or generator is not the source of truth. Jira is the source of truth. Every test scenario must be grounded in the issue description, metadata, or requirement-like bullets.

## Current Project Reality
The SCRUM-6 issue is a PRD-style Jira description rather than a short user story. The real requirement-bearing content sits inside headings like Functional Requirements and Login Process, while business overview text should be ignored.

## Behavioral Rules
1. Never invent business logic.
2. Never create a test case without a Jira requirement anchor.
3. Prefer requirement bullets over marketing or persona text.
4. Keep output deterministic and auditable.
5. If data is missing or ambiguous, report the gap instead of guessing.
6. Use the issue summary, description, and labels as evidence.
7. Treat Jira and its issue fields as the only reliable product source.
8. Generate positive, validation, negative, and boundary test coverage.
9. Keep scope, assumptions, risks, and traceability sections in the final output.
10. Export generated artifacts in HTML, Markdown, JSON, Word, and PDF formats.
11. Use LLM output only to enhance objective, scope, and risks; requirements and test cases remain Jira-grounded.
12. When optional LLM enhancement fails, return the deterministic plan instead of failing the request.

## Data Schema: Jira Input Schema

```json
{
  "issue_key": "string",
  "project_key": "string",
  "summary": "string",
  "description": "string",
  "issue_type": "string",
  "priority": "string",
  "status": "string",
  "assignee": "string",
  "labels": ["string"],
  "components": ["string"],
  "acceptance_criteria": ["string"],
  "comments": ["string"],
  "linked_issues": ["string"],
  "raw_jira_response": {}
}
```

## Data Schema: Test Plan Output Schema

```json
{
  "issue_key": "string",
  "project": "string",
  "objective": "string",
  "scope": ["string"],
  "assumptions": ["string"],
  "risks": ["string"],
  "test_cases": [
    {
      "id": "string",
      "title": "string",
      "category": "string",
      "preconditions": ["string"],
      "steps": ["string"],
      "expected_result": "string"
    }
  ],
  "traceability": {
    "source": "Jira issue data",
    "coverage": ["string"]
  }
}
```

## Architecture Guidance
The project follows the B.L.A.S.T. workflow and the A.N.T. architecture model.

### Layer 1: Architecture
This layer contains the rules and SOPs.
- Jira is source of truth.
- Requirements must be traceable.
- Output must be formal and structured.
- Business logic must not be invented.

### Layer 2: Navigation
This layer orchestrates the process.
- Validate env configuration.
- Fetch the issue from Jira.
- Parse the description into requirement items.
- Generate test case categories.
- Validate the final artifact.

### Layer 3: Tools
This layer contains the deterministic scripts.
- Jira client
- requirement parser
- test-plan generator
- validation utility
- Markdown exporter
- Word/PDF exporter
- local Streamlit and Vercel FastAPI interfaces

## Operational Rules for This Project
- Only use Jira fields that are actually needed.
- Keep tokens in environment variables.
- Use basic-auth Jira calls to the REST API.
- Build requirement extraction around headings and bullet lists.
- Remove persona and business-goal text before generating tests.
- Use explicit categories like Positive, Validation, Negative, and Boundary.
- Keep assumptions and risks in the output so the plan stays honest.
- Use `openai/gpt-oss-20b` as the validated Groq model unless an available model is explicitly configured.
- Do not use local Ollama from a Vercel deployment.

## Example Behavior Contract
The agent should say things like:
- “I fetched the live Jira issue details.”
- “I filtered out product overview content and kept the requirement bullets.”
- “I generated test cases from each requirement group.”
- “I included assumptions and risks instead of guessing at hidden business logic.”

## Final Rule
The generated test plan is valid only when it is backed by Jira evidence, organized clearly, and limited to requirements that can be traced to the original issue.
