# Findings: Jira-Driven Test Plan Creation

## Core Finding
The most reliable method is to treat Jira as the source of truth and convert the issue description into a normalized requirement model before generating test cases.

For the current project, this was confirmed with the live SCRUM-6 issue. The issue is a PRD-like description, not a short user story, so the parser must identify actual requirement bullets and ignore business overview text.

## Important Observations

### 1. Jira issue bodies may be PRD-style, not just acceptance criteria
The live SCRUM-6 issue contains sections such as:
- Executive Summary
- Target Users
- Business Objectives
- Functional Requirements
- Authentication System
- Login Process
- User Input Validation

This means the parser needs to detect the correct section and ignore generic product narrative.

### 2. The best requirement signal is usually in bullet points inside functional sections
The useful requirement items are things like:
- Primary Authentication: Email and password-based login with secure validation
- Session Management: Secure session handling with configurable timeout periods
- Multi-Factor Authentication: Optional 2FA support for enhanced security
- Real-time Validation: Field validation on blur to provide immediate feedback

These are direct signals for valid QA test cases.

### 3. Overview and user segmentation text should not become tests
The parser must skip items like:
- Primary Users: Digital marketers, product managers ...
- Ensure secure access to VWO's experimentation platform
- Minimize login friction to improve user adoption and retention

These are business or persona descriptions, not testable requirements.

## Verified Jira API Calls

### Issue retrieval
```bash
curl -s \
  -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/2/issue/SCRUM-6?fields=summary,description,status,priority,labels,assignee,project,issuetype"
```

### Search by JQL
```bash
curl -s \
  -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/2/search?jql=project=SCRUM AND issuekey='SCRUM-6'&fields=summary,description,status,priority,labels,assignee,project"
```

### Live validation used in this project
```bash
python tools/validate_jira_connection.py --issue-id SCRUM-6
```

## Verified Live Result
The actual project successfully authenticated and retrieved the issue:
- status code: 200
- issue key: SCRUM-6
- summary: VWO LOgin page requirement

## Recommended Parsing Strategy
1. Read the Jira issue JSON.
2. Extract the description body.
3. Detect headings such as Functional Requirements and Login Process.
4. Keep bullet items inside those sections.
5. Exclude target-user, business-objective, and marketing text.
6. Convert the remaining items into QA requirements.
7. Convert those into test-case categories: positive, validation, negative, boundary.

## Example requirement model
```json
{
  "issue_key": "SCRUM-6",
  "summary": "VWO LOgin page requirement",
  "acceptance_criteria": [
    "Primary Authentication: Email and password-based login with secure validation",
    "Real-time Validation: Field validation on blur to provide immediate feedback",
    "Forgot Password Flow: Streamlined password reset process with secure token generation"
  ]
}
```

## Final Finding
The system works best when it treats Jira descriptions as structured PRD text and then extracts only requirement-bearing bullets. This is the core pattern used by the current project and it has been validated live against SCRUM-6.

## Delivery Findings
- The local Streamlit interface at http://localhost:8502/ accepts Jira references directly.
- The Vercel deployment is available at https://jira-test-plan-generator.vercel.app.
- Vercel cannot access local Ollama, so hosted AI enhancement uses Groq model `openai/gpt-oss-20b`.
- The configured account returned 404 for `llama-3.3-70b-versatile`; `openai/gpt-oss-20b` was validated with HTTP 200.
- Groq enhancement is optional. If it fails, the deterministic Jira-backed plan is still returned.
- Download artifacts were validated as valid Word (`PK` header) and PDF (`%PDF` header) documents.
