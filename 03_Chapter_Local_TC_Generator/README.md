# Chapter 03: Local Test Case Generator

This chapter implements a local Jira-to-test-case workflow that turns requirement text into QA-ready work products.

## Goal
Generate quality test cases from Jira issues without guessing business logic.

## What it does
- fetches Jira issue information
- normalizes requirement content
- extracts requirement statements from PRD-like issue text
- builds QA test cases
- exports markdown, CSV, or other artifact formats
- optionally calls Ollama or Groq for enhancement

## Core flow
```text
Jira issue -> requirement parser -> test case generator -> export artifact
```

## Example usage
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\03_Chapter_Local_TC_Generator"
python -m uvicorn api.index:app --host 0.0.0.0 --port 8000
```

Or use the local Streamlit UI:
```powershell
cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\03_Chapter_Local_TC_Generator\src"
python -m streamlit run app.py
```

## Example prompt
```text
create test cases for SCRUM-6
```

## Important design rule
The app should reject noisy product-summary text and keep only requirement-backed statements that can be tested.

## Output types
- CSV
- Excel
- Markdown
- JSON-ready structured results

## Key files
- api/index.py
- src/app.py
- src/jira_client.py
- src/llm_client.py
- src/exporter.py
- src/templates/test_case_template.md
- Results/

## Takeaway
This chapter demonstrates a realistic local AI testing workflow where the model helps generate output, but the requirement source remains traceable and auditable.
