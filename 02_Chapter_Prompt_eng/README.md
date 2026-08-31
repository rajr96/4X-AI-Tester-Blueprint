# Chapter 02: Prompt Engineering

This chapter covers prompt design patterns for structured, repeatable AI workflows in software testing and automation.

## Objective
Turn vague requests into deterministic outputs that are easier to validate and use in real projects.

## Included materials
- 00_Task1.md
- 01_Rice_POT_Template.md
- 02_RICE_Pot_example.md
- 04_Plan_Framework.md
- 05_Salesforce_Login_Test_Cases.md
- Rice_Pot_SeleniumAdvanceFramework/

## Core prompt patterns

### 1. Role + task + constraints
This pattern improves result quality by setting scope and boundaries.

Example:
```text
You are a senior QA engineer.
Create a test plan for the login workflow.
Use only the requirement text provided.
Do not invent features.
Return a list of test cases with steps and expected results.
```

### 2. RICE / POT structure
Useful for planning and prioritization.

Example:
```text
R: Reach
I: Impact
C: Confidence
E: Effort

P: Problem
O: Options
T: Test
```

### 3. Structured output requirement
Ask the model to return JSON, markdown, or table-based results so the content is easier to validate.

Example:
```json
{
  "summary": "Login validation",
  "test_cases": [
    { "id": "TC-01", "steps": ["Open login page", "Enter valid credentials"], "expected_result": "User signs in successfully" }
  ]
}
```

## Example workflow
```text
Create QA test cases for a Salesforce login screen.
Include:
- happy path
- invalid password
- missing email
- error message validation
- session timeout behavior
Return results in markdown.
```

## Why this matters
Prompt quality directly affects:
- requirement coverage
- test accuracy
- reusability of the workflow
- trust in AI-generated QA artifacts

## Takeaway
Prompt engineering is not about using fancy phrasing. It is about clarity, constraints, and validation rules that align the AI output with the target system.
