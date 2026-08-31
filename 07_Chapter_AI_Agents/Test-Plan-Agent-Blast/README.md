# Jira Test Plan Creator

A Python application that turns a Jira issue key into a structured, traceable QA test plan. It reads a Jira issue, extracts requirement statements, and provides downloadable Markdown, JSON, HTML, Word, and PDF artifacts.

## Current status
The project is deployed and operational:
- Jira authentication is validated against the live Atlassian API.
- A real issue such as SCRUM-6 can be fetched successfully.
- The parser filters out non-requirement PRD text and keeps functional requirement bullets.
- The generator creates requirement-based test cases plus negative and boundary coverage.
- The local Streamlit app accepts a Jira reference and generates the plan automatically.
- The Vercel web app is available at https://jira-test-plan-generator.vercel.app.
- The deployed app generates HTML, Markdown, JSON, Word, and PDF downloads.

## Project goal
Create a deterministic test plan generator from a Jira issue ID, grounded in actual Jira requirement data instead of guessed product behavior.

## Architecture
The project follows the BLAST + A.N.T. model:
- Architecture: rules, schemas, and documentation
- Navigation: orchestration and validation flow
- Tools: Python scripts for Jira access, parsing, and generation

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables.
   The project currently supports:
   - root-level .env
   - tools/.env

   Example:
   ```bash
   copy .env.example .env
   ```

   Or edit the live file in the tools folder.

4. Update values in the environment file:
   ```env
   JIRA_BASE_URL=https://your-company.atlassian.net
   JIRA_EMAIL=you@example.com
   JIRA_TOKEN=your_api_token
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=gemma3:1b
   GROQ_API_TOKEN=your_groq_api_key
   GROQ_MODEL=openai/gpt-oss-20b
   LLM_PROVIDER=ollama
   ```

   The local app supports Ollama and Groq. The Vercel deployment uses Groq only because it cannot reach a local Ollama service. Add Vercel environment variables through the Vercel dashboard or CLI; never commit secrets.

## Usage

Start the local test-plan generator:

```bash
streamlit run streamlit_app.py
```

Open http://localhost:8502/, enter a Jira request such as `Create a test plan for SCRUM-6`, and select either Ollama or Groq from the settings panel. The app fetches the issue, creates the plan automatically, and provides Markdown, JSON, HTML, Word, and PDF downloads.

Use the deployed application at https://jira-test-plan-generator.vercel.app. It uses the configured Groq model for optional enhancement and always falls back to the deterministic Jira-backed plan if AI enhancement is unavailable.

Run the project for a Jira issue key:

```bash
python app.py --issue-id SCRUM-6 --output output/test-plan.md
```

Validate Jira connectivity separately:

```bash
python tools/validate_jira_connection.py --issue-id SCRUM-6
```

## What the project does
- Fetches a Jira issue by key
- Reads summary, status, priority, and description
- Parses requirement-style bullets from Jira PRD text
- Removes target-user and business-objective noise
- Produces a test plan with positive, validation, negative, and boundary scenarios
- Optionally enriches the objective, scope, and risks using the configured Ollama or Groq model
- Exports HTML, Markdown, JSON, Word, and PDF artifacts

## Real-world findings from SCRUM-6
The live issue is a product requirements document, not a short story. It contains headings like:
- Executive Summary
- Target Users
- Business Objectives
- Functional Requirements
- Authentication System
- Login Process
- User Input Validation

This means the parser must be careful to keep only requirement-based content and ignore overview/marketing sections.

## Output example
The generated output includes:
- Scope
- Assumptions
- Risks
- Traceability
- Test cases

## Notes
- The project intentionally avoids generating business logic that is not grounded in Jira data.
- Missing or ambiguous issue details are reported as gaps instead of being guessed.
- The live Jira prototype is working for SCRUM-6 and can be extended to other issue IDs.
