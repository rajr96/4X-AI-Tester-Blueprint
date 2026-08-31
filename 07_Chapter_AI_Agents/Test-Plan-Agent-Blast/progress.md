# Progress Log: Jira Test Plan Creator

## Project State
The project is now in the working prototype stage. It can connect to Jira, fetch live issue data, parse requirement-style content, and generate a structured Markdown test plan.

## 2026-08-31

### 09:00
- Created the BLAST-based project scope.
- Confirmed that the objective is to generate a test plan from a Jira issue ID.
- Result: initial planning artifacts were created in the project folder.

### 09:15
- Reviewed the BLAST protocol and confirmed the need for Protocol 0 artifacts before implementation.
- Identified the key rule: never guess business logic without Jira evidence.
- Result: the project was built around a source-of-truth approach.

### 09:30
- Defined the likely Jira API workflow: fetch issue -> parse description -> normalize requirements -> generate tests.
- Result: a basic architecture and task plan were documented.

### 09:45
- Drafted the first versions of the task plan and findings documents.
- Result: the project had a clear path for the Link and Architect phases.

### 10:00
- Added example Jira REST calls and planned how to extract issue fields.
- Result: the API contract and required fields were documented.

### 10:15
- Started working on the project constitution in LLM.md.
- Result: the architecture and rules were defined before tool implementation.

### 10:30
- Created the first runnable project skeleton with Python app, Jira client, parser, and generator.
- Result: the project moved from concept to executable prototype.

### 11:00
- Moved to live validation.
- Error found: .env was not being loaded from the tools folder, which blocked live Jira use.
- Fix: app.py now loads the env file from either project root or tools/.env.
- Result: the project successfully authenticated to Jira.

### 11:15
- Tested the live Jira endpoint for SCRUM-6.
- Result: HTTP 200 returned, confirming that the Jira credentials and base URL were valid.

### 11:30
- Parsed the live SCRUM-6 issue description.
- Finding: the Jira issue is a PRD with headers like Target Users, Business Objectives, Functional Requirements, and Login Process.
- Result: the parser had to be improved to ignore non-requirement text and extract the actionable requirement items.

### 11:45
- Updated the requirement parser to filter out PRD overview content and preserve requirement bullets.
- Result: the extracted acceptance criteria became relevant to functional QA.

### 12:00
- Updated the generator to create requirement-based test cases and additional negative/boundary scenarios.
- Result: the artifact became more meaningful and closer to a formal QA plan.

### 12:15
- Ran the unit tests for the client, parser, and generator.
- Result: 4 tests passed successfully.

### 12:30
- Ran the final end-to-end workflow against SCRUM-6.
- Result: output/test-plan.md was generated successfully and the project is working end-to-end.

### 13:00
- Added a local Streamlit interface that accepts a Jira reference and generates plans automatically.
- Result: local generator is available at http://localhost:8502/.

### 13:15
- Added and deployed a Vercel-compatible FastAPI application.
- Result: production app is available at https://jira-test-plan-generator.vercel.app.

### 13:30
- Diagnosed Groq HTTP 404 for `llama-3.3-70b-versatile` and selected validated model `openai/gpt-oss-20b`.
- Result: real Groq model request returned HTTP 200; deterministic generation remains available if optional enhancement fails.

### 13:45
- Added Word and PDF test-plan exports and improved the hosted AI enhancement toggle.
- Result: live SCRUM-6 production generation returned valid DOCX (`PK`) and PDF (`%PDF`) downloads; 12 regression tests passed.

## Logging Rules
- Every milestone should include action, issue, fix, and result.
- Every API validation should record status code and endpoint.
- Every parser update should note what was excluded and what was kept.
- Every generator enhancement should specify whether the output became more test-ready.

## Current Status
The project is deployed and validated: Jira integration, requirement parsing, deterministic plan creation, optional Groq enhancement, and all five output formats are working from the local and Vercel interfaces.
