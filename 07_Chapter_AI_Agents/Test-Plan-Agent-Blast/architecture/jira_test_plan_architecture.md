# Jira Test Plan Creator Architecture

## 1. Purpose
This project turns a Jira issue key into a deterministic test plan for QA and release validation.

## 2. Architecture Layers

### Layer 1: Architecture
The project defines explicit rules:
- Jira is the only source of truth for requirement facts.
- The LLM or generator may not invent requirements.
- The pipeline must remain explicit, traceable, and exportable.
- All generated tests should map back to a Jira issue or acceptance criterion.

### Layer 2: Navigation
The workflow orchestrates the process:
1. Accept issue key.
2. Load Jira env config.
3. Fetch issue and related fields.
4. Parse the description into requirement blocks.
5. Extract acceptance criteria.
6. Build a normalized requirement model.
7. Generate a test plan.
8. Save the result to Markdown or CSV.

### Layer 3: Tools
The tools layer contains deterministic Python functions:
- Jira REST client
- requirement parser
- test-plan generator
- validation script
- exporter

## 3. Data Flow
Jira issue JSON -> requirement parser -> test plan generator -> output artifact

## 4. Validation Rules
- 401/403 errors must be treated as auth issues.
- 404 means the issue key or Jira base URL is wrong.
- Missing acceptance criteria should produce a warning, not a guessed requirement.
- All outputs should include traceability to the source issue.

## 5. Output Contract
The final output is a Markdown test plan containing:
- summary
- objective
- test cases
- expected results
- risk notes
- issues or open questions

## 6. Implementation Notes
The project keeps everything deterministic and explicit. It avoids freestyle generation and instead works from a structured issue model.
