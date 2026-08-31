# Task Plan: Jira Test Plan Creator

## Objective
Create a deterministic agent workflow that takes a Jira issue ID, fetches issue details, extracts the relevant requirement statements from the issue description, and produces a structured QA test plan.

## Primary Goal
Build a project that can answer:
- Which Jira issue is being tested?
- What business or functional requirements exist?
- Which requirement statements should become test cases?
- What risk and boundary scenarios should be included?
- What final Jira-backed test-plan artifact should be produced?

## Success Criteria
- A user can provide a Jira issue key such as SCRUM-6.
- The system connects to Jira successfully using credentials from the environment.
- The system can parse requirement-like bullets from a PRD-style Jira description.
- The output includes a QA-style structure with scope, assumptions, risks, traceability, and test cases.
- The project is deterministic, auditable, and explainable.

## Phase Summary

### Phase 0: Initialization
- [x] Define scope and constraints.
- [x] Create the planning and constitution files.
- [x] Confirm the project is source-of-truth driven by Jira.

### Phase 1: Blueprint
- [x] Clarify the issue-to-test-plan workflow.
- [x] Decide on the requirement parsing strategy.
- [x] Define the target output structure.

### Phase 2: Link
- [x] Verify Jira connectivity with valid API credentials.
- [x] Validate a real Jira issue lookup against SCRUM-6.
- [x] Confirm endpoint and authentication behavior.

### Phase 3: Architect
- [x] Build the architecture split into architecture, navigation, and tools layers.
- [x] Build the Jira client, parser, and generator.
- [x] Validate live output generation.

### Phase 4: Stylize / Finalize
- [x] Improve the output structure with scope, assumptions, risks, and traceability.
- [x] Produce a more formal Markdown test plan.
- [x] Confirm the artifact is readable and auditable.
- [x] Add a local Jira-reference web interface with downloadable test-plan artifacts.
- [x] Deploy the FastAPI web application to Vercel.
- [x] Add Groq enhancement with deterministic fallback.
- [x] Add HTML, Markdown, JSON, Word, and PDF downloads.

## Checklist

### Discovery / Scope
- [x] Confirm primary objective: create a Jira-based test plan.
- [x] Confirm issue source: Jira Cloud.
- [x] Confirm auth method: Jira API token via basic auth.
- [x] Confirm delivery format: Markdown artifact.
- [x] Confirm single issue flow is the baseline use case.

### Data Extraction
- [x] Identify relevant fields: summary, description, status, priority, project, issue type.
- [x] Parse unstructured Jira descriptions into requirement items.
- [x] Filter out business overview and user-profile content.
- [x] Keep requirement-like product and validation bullets as test inputs.

### API and Connectivity
- [x] Validate environment variables for Jira URL, email, and token.
- [x] Validate issue retrieval endpoint.
- [x] Confirm successful live connection to SCRUM-6.
- [x] Validate error handling and env loading logic.

### Test Plan Generation
- [x] Define the formal output structure.
- [x] Map requirement items to test-case groups.
- [x] Generate positive, negative, and boundary scenarios.
- [x] Include steps, expected results, assumptions, and risks.
- [x] Include traceability notes back to Jira.

### Quality Gates
- [x] Avoid guessing business logic.
- [x] Keep the output tied to Jira requirements.
- [x] Make the artifact readable and structured.
- [x] Save the result in a reproducible format.

## Current Working Plan
1. Read a Jira issue by ID.
2. Fetch the issue description and metadata.
3. Extract requirement-like items from the PRD.
4. Normalize the requirement list into a test model.
5. Produce a formal QA test plan.
6. Export the result as HTML, Markdown, JSON, Word, or PDF.

## Dependencies
- Jira base URL
- Jira email and API token
- Python environment with requests and python-dotenv
- Test-plan artifact output path

## Risks and Constraints
- Jira descriptions can be PRD-like and unstructured.
- Business overview text can be mistaken for requirements.
- Some issues may have missing or ambiguous acceptance criteria.
- Real issue data must be treated as the source of truth.

## Deliverables
- task_plan.md
- findings.md
- progress.md
- LLM.md
- architecture notes
- Jira validation script
- app.py and generator logic
- local Streamlit UI and Vercel FastAPI UI
- generated HTML, Markdown, JSON, Word, and PDF outputs

## Current Status
The project is deployed at https://jira-test-plan-generator.vercel.app and supports a local Streamlit UI at http://localhost:8502/. It can authenticate to Jira, fetch a live issue, parse requirement-style text, and generate downloadable structured test-plan artifacts.
