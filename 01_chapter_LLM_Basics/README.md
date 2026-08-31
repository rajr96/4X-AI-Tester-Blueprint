# Chapter 01: LLM Basics

This chapter focuses on understanding how large language models behave, where they fail, and how to use them responsibly in QA and automation work.

## Objective
Build a strong mental model for:
- hallucinations and uncertainty
- prompt sensitivity
- output validation
- safe human-in-the-loop review

## Core ideas

### 1. LLMs predict text, not truth
The model does not "know" facts in the same way as a database or rule engine. It generates the most statistically likely continuation for a prompt.

Example:
```text
Prompt: What is the release date of Project X?
Model answer: "It is scheduled for Q4."
Risk: The answer may be fabricated unless grounded in real source data.
```

### 2. Grounding matters
When the task requires precision, the model should be fed source material and validated outputs.

Example:
```text
Use Jira issue text, requirements docs, or code comments as inputs.
Then validate the generated tests against the requirement before shipping them.
```

### 3. Prompts change behavior dramatically
Small wording changes can shift model focus or confidence.

Example:
```text
Weak: Write test cases for the login flow.
Strong: Based only on the Jira requirement list below, create QA test cases that cover happy path, validation, and negative states.
```

## Practical anti-hallucination pattern
1. Ask for a grounded answer
2. Require evidence or source references
3. Validate output against source material
4. Reject unsupported assumptions

## Example exercise
```text
Given the following requirement:
- A user must sign in with a valid email and password.
- Invalid credentials must show an error message.

Generate test cases that only cover what is explicitly stated.
Do not invent extra flows.
```

## Suggested outputs
- summary of the risk
- fact-checking notes
- improved prompts
- validated QA steps

## Files in this chapter
- ch_01_anti_hallucination.md

## Takeaway
The safest AI workflow is one where the model generates ideas, but humans and explicit validation rules check the result before it becomes a deliverable.
