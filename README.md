# 4X AI Tester Blueprint

## Repository goal
This repository is a structured learning and implementation blueprint for building AI-driven test generation, QA automation, and job-application tooling using local and cloud AI workflows.

It combines:
- LLM fundamentals and prompt engineering
- Local test-case generation from Jira requirements
- Resume and job matching workflows
- Job tracking dashboards
- Brand and LinkedIn content repurposing
- AI agent orchestration for testing tasks

## Quick git workflow
Use this command prompt to perform the full git workflow:

```text
go go go:
1. Update parent README file.
2. Add all files.
3. Commit all changes.
4. Push code to https://github.com/rajr96/4X-AI-Tester-Blueprint.git
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

What is included:
- LLM basics and reliability guidance
- Hallucination prevention patterns
- Prompting concepts and testing discipline

Example use:
```text
Summarize the risk of using an LLM without validation for production QA decisions.
```

### 02_Chapter_Prompt_eng
Focus: structured prompt design and frameworks for better task execution.

What is included:
- RICE / POT prompt templates
- Planned prompt flows for QA and automation tasks
- Example login and Salesforce test-case prompt patterns
- Prompt engineering strategies for clearer output

Example use:
```text
Create a QA prompt that turns a Jira requirement into test cases with validation, negative, and boundary coverage.
```

### 03_Chapter_Local_TC_Generator
Focus: local Jira-to-test-case generation using Python, LLMs, and export workflows.

What is included:
- Jira issue fetching and requirement parsing
- Local prompt templates for test case generation
- Ollama-first local AI flow with Groq fallback
- CSV/Excel export for generated test cases
- Settings screen and environment-based configuration

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
- pages/settings.py
- config_store.py
- jira_client.py
- llm_client.py
- exporter.py
- templates/test_case_template.md
- Results/

### 04_Chapter_JobKitAI
Focus: AI-assisted job search and resume optimization.

What is included:
- Job description intake and matching workflows
- Resume tailoring for roles and ATS alignment
- Structured outputs for application preparation

Example use:
```text
Tailor my resume to a Senior QA Automation Engineer role using the job description and my skill profile.
```

### 05_Chapter_JobTrackerAI
Focus: job application tracking and dashboarding in a browser app.

What is included:
- Vite + React job tracker UI
- Job cards, modal details, and application status tracking
- A lightweight local AI productivity workflow for job management

Local start:
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\05_Chapter_JobTrackerAI"
npm run dev -- --host 0.0.0.0 --port 4173
```

Local URL:
```text
http://localhost:4173/
```

### 06_Chapter_Branding_LinkedinSkills
Focus: branding, content repurposing, and personal positioning for professional visibility.

What is included:
- Personal brand guidance
- LinkedIn content packages
- Positioning and repurposing templates

Example use:
```text
Turn a project summary into a LinkedIn post, a short article, and a personal brand narrative.
```

### 07_Chapter_AI_Agents
Focus: agentic workflows and structured AI planning for testing and QA tasks.

What is included:
- Test plan generation from Jira issues
- Agent-style task plans and prompt packing
- Exportable generation outputs
- Deterministic requirement extraction before optional AI enhancement

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
Focus: reusable notes, standards, and supporting materials across the blueprint.

What is included:
- Anti-hallucination rules
- Prompt comparison notes
- Requirements and reference documents for learning and reuse

## Verified working apps

### 1) JobTracker (Vite + React)
- Local URL: http://localhost:4173/
- Vercel production URL: https://jobtrackerai-five.vercel.app
- Project folder: 05_Chapter_JobTrackerAI

### 2) Jira Test Case Generator (FastAPI + Vercel)
- Local URL: http://localhost:8501/ (Streamlit dev mode)
- Vercel production URL: https://jira-test-case-generator-delta.vercel.app
- Project folder: 03_Chapter_Local_TC_Generator

### 3) Jira Test Plan Generator (FastAPI + Vercel)
- Local URL: http://localhost:8502/
- Vercel production URL: https://jira-test-plan-generator.vercel.app
- Project folder: 07_Chapter_AI_Agents/Test-Plan-Agent-Blast

## Quick examples

### Example 1: Local test case generation
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\03_Chapter_Local_TC_Generator\src"
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Use a prompt such as:
```text
create test cases for SCRUM-6
```

### Example 2: Job tracker app
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\05_Chapter_JobTrackerAI"
npm run dev -- --host 0.0.0.0 --port 4173
```

### Example 3: Test plan generation
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\07_Chapter_AI_Agents\Test-Plan-Agent-Blast"
python app.py --issue-id SCRUM-6 --output output/test-plan.md
```

## Latest delivery summary
The blueprint includes working local and deployed tools for:
- AI-assisted test case creation
- Jira requirement parsing into QA coverage
- Job search and matching support
- Personal-brand content workflows
- QA planning with structured exports

The Jira Test Plan Generator is a concrete example of deterministic testing: it extracts requirements from Jira data, rejects PRD noise, and builds test coverage before optional AI enrichment.

- Last synchronized: 2026-08-31
