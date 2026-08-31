# Chapter 07: AI Agents

This chapter focuses on agent-style workflows that orchestrate planning, validation, and generation for QA tasks.

## Goal
Build repeatable flows that take a request like a Jira issue key and convert it into a structured QA artifact.

## Included project
- Test-Plan-Agent-Blast/

## Example workflow
```text
Input: SCRUM-6
Process: fetch Jira issue -> parse requirement statements -> generate QA test plan -> export HTML/Markdown/JSON
```

## Local run
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\07_Chapter_AI_Agents\Test-Plan-Agent-Blast"
python -m streamlit run streamlit_app.py --server.address localhost --server.port 8502
```

## Example command
```powershell
python app.py --issue-id SCRUM-6 --output output/test-plan.md
```

## Design principles
- keep the requirement source grounded in Jira
- filter out PRD and overview noise
- build deterministic test coverage first
- use optional LLM enhancement only for non-source-of-truth metadata

## Outputs
- Markdown test plan
- HTML report
- JSON export
- optional AI-enhanced objective/scope/risk metadata

## Takeaway
This chapter demonstrates an agentic QA workflow: a system that reads a real issue, extracts testable requirements, and produces a structured QA delivery artifact.
