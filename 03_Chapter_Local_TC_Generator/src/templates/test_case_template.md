# Test Case Generation Request

Create concise, executable QA test cases for Jira issue `{{key}}`.

## Jira Summary
{{summary}}

## Description
{{description}}

## Acceptance Criteria
{{acceptance_criteria}}

## Output Rules

Return Markdown. For each test case include:
- ID and title
- Priority and type
- Preconditions and test data
- Numbered steps with an expected result for every step
- Overall expected result
- Assumptions or coverage gaps

Do not invent requirements. Mark missing details as assumptions or coverage gaps.