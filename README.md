# 4X AI Tester Blueprint

## Repository goal
This repository is a structured learning and implementation blueprint for building AI-powered QA, test generation, agile workflows, job tooling, and productivity automation.

It combines:
- LLM fundamentals and anti-hallucination discipline
- Prompt engineering and workflow design
- Local Jira-to-test-case generation
- Job search and resume tailoring workflows
- Job tracking dashboards and task management
- Personal brand and LinkedIn content repurposing
- AI agent-style testing orchestration

## Quick git workflow
Use this sequence for updates and publication:

```text
1. Update parent README.md
2. Review all key files and app changes
3. Add files to git
4. Commit all changes
5. Push to https://github.com/rajr96/4X-AI-Tester-Blueprint.git
```

## Repository structure
- 01_chapter_LLM_Basics
- 02_Chapter_Prompt_eng
- 03_Chapter_Local_TC_Generator
- 04_Chapter_JobKitAI
- 05_Chapter_JobTrackerAI
- 06_Chapter_Branding_LinkedinSkills
- 07_Chapter_AI_Agents
- References

## Chapter-wise summary

### 01_chapter_LLM_Basics
Focus: AI fundamentals, model behavior, prompting intuition, and anti-hallucination thinking.

Included:
- LLM basics and reliability guidance
- Hallucination prevention patterns
- Prompting concepts and testing discipline

Example use:
```text
Summarize the risk of using an LLM without validation for production QA decisions.
```

### 02_Chapter_Prompt_eng
Focus: structured prompt engineering and reusable QA frameworks.

Included:
- RICE and POT prompt templates
- Salesforce and login-case QA prompt examples
- Plan-based prompt design for better reasoning and output quality

Example use:
```text
Create a QA prompt that converts a Jira requirement into test cases with validation, negative, and boundary coverage.
```

### 03_Chapter_Local_TC_Generator
Focus: Jira-to-test-case generation using Python, local AI workflows, and export features.

Included:
- Jira issue fetch and parsing logic
- Local prompt templates for QA generation
- Ollama-first local AI flow with Groq fallback
- CSV and Excel export generation
- Settings screen and environment-based configuration
- Runtime fallback handling for stale Jira secrets

Example workflow:
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\03_Chapter_Local_TC_Generator"
python -m uvicorn api.index:app --host 0.0.0.0 --port 8000
```

Example prompt:
```text
create test cases for SCRUM-6
```

Key files:
- app.py
- api/index.py
- src/config_store.py
- src/jira_client.py
- src/llm_client.py
- src/exporter.py
- src/templates/test_case_template.md
- src/Results/

### 04_Chapter_JobKitAI
Focus: AI-assisted job search and resume optimization.

Included:
- Job description intake and matching workflows
- Resume tailoring for ATS and role alignment
- Structured output for application preparation

Example use:
```text
Tailor my resume to a Senior QA Automation Engineer role using the job description and my skill profile.
```

### 05_Chapter_JobTrackerAI
Focus: job application tracking and dashboarding in a browser app.

Included:
- Vite + React job tracker UI
- Kanban board with status grouping and filters
- Job cards, modals, and application tracking
- Modern design and UX improvements

Local start:
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\05_Chapter_JobTrackerAI"
npm install
npm run dev -- --host 0.0.0.0 --port 4173
```

Local URL:
```text
http://localhost:4173/
```

### 06_Chapter_Branding_LinkedinSkills
Focus: branding, content repurposing, and professional positioning.

Included:
- Personal brand guidance
- LinkedIn content packages
- Repurposing templates for posts and thought leadership

Example use:
```text
Turn a project update into a LinkedIn post, article outline, and personal brand narrative.
```

### 07_Chapter_AI_Agents
Focus: agentic workflows and structured AI planning for testing and QA tasks.

Included:
- Test plan generation from Jira issues
- Agent-style prompt workflows and task planning
- Exportable test plan generation
- Requirement extraction before optional AI enhancement

Local start:
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\07_Chapter_AI_Agents\Test-Plan-Agent-Blast"
python -m streamlit run streamlit_app.py --server.address localhost --server.port 8502
```

Example input:
```text
SCRUM-6
```

### References
Focus: reusable notes, standards, and supporting reference materials.

Included:
- Anti-hallucination rules
- Prompt comparison notes
- Supporting docs and references for long-term learning

## Verified working apps

### 1) JobTracker (React + Vite)
- Local URL: http://localhost:4173/
- Vercel URL: https://jobtrackerai-five.vercel.app
- Project folder: 05_Chapter_JobTrackerAI

### 2) Jira Test Case Generator (FastAPI + Vercel)
- Local Streamlit URL: http://localhost:8501/
- Vercel URL: https://jira-test-case-generator-delta.vercel.app
- Project folder: 03_Chapter_Local_TC_Generator

### 3) Jira Test Plan Generator (Streamlit)
- Local URL: http://localhost:8502/
- Project folder: 07_Chapter_AI_Agents/Test-Plan-Agent-Blast

## Quick examples

### Example 1: Local Jira test case generation
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\03_Chapter_Local_TC_Generator\src"
python -m streamlit run app.py
```

Use a prompt such as:
```text
create test cases for SCRUM-6
```

### Example 2: Job tracker app
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\05_Chapter_JobTrackerAI"
npm install
npm run dev -- --host 0.0.0.0 --port 4173
```

### Example 3: Test plan generation
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\07_Chapter_AI_Agents\Test-Plan-Agent-Blast"
python -m streamlit run streamlit_app.py --server.address localhost --server.port 8502
```

## Deployment and troubleshooting notes
The project includes a worked example of handling a live production failure caused by stale Jira credentials in Vercel. The fix path included:
- verifying the Jira token directly against the Jira REST API
- updating the app to accept alternate environment variable names
- adding a fallback retry strategy for stale Production secrets
- verifying the deployment source and rebuild flow

## Latest delivery summary
The repository now includes working examples and tooling for:
- AI-assisted test case creation and export
- Jira requirement parsing into QA coverage
- Job matching and application tracking
- AI-driven personal brand and content packaging
- Agentic QA planning flows

- Last synchronized: 2026-09-01
