## **Hallucinations (LLMs “Making Things Up”)**
### **Definition** 
A hallucination occurs when an AI model produces confident but factually incorrect or completely fabricated output, even though the information does not exist in the system, logs, API, or requirements.

The key danger: **the answer sounds correct**.



### **<u>QA Example 1 : Bug Report Hallucination</u>**
**Prompt to AI**

“Analyze this screenshot and generate a Jira bug report.”

**AI Output (Hallucinated)**

- Error Code: AUTH_403_INVALID_TOKEN
- Root Cause: Token expiry after 15 minutes
- Affected API: /auth/refresh


**Reality**

- Screenshot only shows “Something went wrong”
- No error code visible
- No token logic involved


**Why this is a hallucination**

- AI **invented technical details**
- No evidence in input
- Over-confident explanation


### **<u>QA Example 2 – Test Case Hallucination</u>**
**Prompt**

“Generate test cases for VWO dashboard.”

**AI Output**

- Test case: Verify **Dark Mode toggle**
- Test case: Validate **Export to CSV**


**Reality**

- No Dark Mode
- No Export feature in product


![image.png](https://eraser.imgix.net/workspaces/bhSR1i1RNhgFLX5vDxgp/WWS31TdyovhjTB1TVo9v2jWpPei1/image_-2OD4_SqXPuUY0qj0aqVk.png?ixlib=js-3.8.0 "image.png")

### **QA Red Flags for Hallucinations**
- Mentions **features not in PRD**
- Invents **error codes**
- Claims **logs show X** (without logs)
- Gives **exact numbers** without evidence
Sounds _too certain_ without sources

---

> You never ask the AI. You always tell the AI what to do.



# Anti-Hallucination Rules
**ROLE:** You are a QA assistant operating under strict verification rules.
SCOPE OF KNOWLEDGE

You may ONLY use information explicitly provided in: 
PRD
API documentation
Logs
Screenshots
Test data
User input



STRICT RULES (MANDATORY)
DO NOT invent features, APIs, error codes, UI elements, or behavior.
DO NOT assume default or "typical" system behavior.
If information is missing or unclear, respond with: "Insufficient information to determine."
Every assertion must be traceable to provided input.
If a detail is inferred, label it explicitly as: "Inference (low confidence)".
Output must be deterministic and repeatable.


PROCESS YOU MUST FOLLOW
Step 1: Extract verifiable facts from the input. 
Step 2: List unknown or missing information. 
Step 3: Generate output ONLY from Step 1 facts. 
Step 4: Perform a self-check for hallucinations or contradictions. 
OUTPUT FORMAT (STRICT)
Verified Facts:
Missing / Unknown Information:
Generated Output:
Self-Validation Check:
If you cannot complete a step, stop and report why. 
>> Instructions  



1. Local LLM with Ollama, LM Studio
2. What is Prompt?, Skill?
3. Prompt vs Skill File vs AI Agents
4. Skill File (Office) - md -> that you can shared. (
    1. Folder skill which can do many things.


## Using the anti-hallucination rule to get the maximum output from the large language model 


Req - [docs.google.com/document/d/1GsT57ocl4HaUCxNhBGVmwvLYh7R24gjVB_RDteltkF4/edit?usp=sharing](https://docs.google.com/document/d/1GsT57ocl4HaUCxNhBGVmwvLYh7R24gjVB_RDteltkF4/edit?usp=sharing) 



Bad EXAMPLE

[chatgpt.com/share/69a3c1a9-3ed0-8009-969c-9dd3a7cce824](https://chatgpt.com/share/69a3c1a9-3ed0-8009-969c-9dd3a7cce824) 



Good Example

PRD - [docs.google.com/document/d/1GsT57ocl4HaUCxNhBGVmwvLYh7R24gjVB_RDteltkF4/edit?usp=sharing](https://docs.google.com/document/d/1GsT57ocl4HaUCxNhBGVmwvLYh7R24gjVB_RDteltkF4/edit?usp=sharing) 

[chatgpt.com/share/69a3c2d9-1f40-8009-98ed-6e04598199b4](https://chatgpt.com/share/69a3c2d9-1f40-8009-98ed-6e04598199b4) 



---

Anti HALLCINATIONS Rule

[github.com/PramodDutta/AI-Tester-Blueprint/blob/main/chapter_01_foundation_model/rules_checklists/ch_01_anti_hallucination.md](https://github.com/PramodDutta/AI-Tester-Blueprint/blob/main/chapter_01_foundation_model/rules_checklists/ch_01_anti_hallucination.md) 


