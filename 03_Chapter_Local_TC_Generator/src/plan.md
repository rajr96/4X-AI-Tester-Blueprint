# Jira Test Case Generator Implementation Plan

## Goal

Create a small Streamlit application that accepts a Jira ticket request in a chat screen, retrieves the ticket, loads a local test-case template, generates structured test cases with Ollama, and uses Groq only when explicitly selected or when Ollama is unavailable.

The application is an internal tool. The implementation will stay modular and use only the dependencies needed for Streamlit, HTTP calls, environment loading, and the selected LLM clients.

## Target File Structure

```text
03_Chapter_Local_TC_Generator/
  src/
    app.py
    config_store.py
    jira_client.py
    llm_client.py
    requirements.txt
    plan.md
    .env.example
    pages/
      settings.py
    templates/
      test_case_template.md
```

The real `.env` file will be supplied locally and will not be committed. `.env.example` will contain variable names and safe placeholder values only.

## Configuration and Secret Handling

1. Load environment variables from `.env` at application startup using `python-dotenv`.
2. Read Jira URL, Jira email, Jira API token, and Groq API key from environment variables. Expected names:
   - `JIRA_BASE_URL`
   - `JIRA_EMAIL`
   - `JIRA_API_TOKEN`
   - `GROQ_API_KEY`
3. Keep non-secret runtime settings in a local configuration file, such as `.config/settings.json`, including the selected provider. The file will be outside version control.
4. Do not write credentials into chat history, generated files, source code, logs, browser state, or the local JSON configuration.
5. Add `.env`, `.config/`, and other local secret/config paths to `.gitignore` before running the application.
6. Use Streamlit password inputs or masked status indicators when showing secret-related settings. Never display token or API-key values after loading them.
7. Validate required configuration before making Jira or LLM requests and return actionable, non-secret error messages.

## Screen Design

### Screen 1: Chat (`app.py`)

- Use Streamlit's chat layout with `st.chat_input` and `st.chat_message`.
- Preserve the current conversation in `st.session_state`.
- Accept requests such as `create test cases for QA-102`.
- Show a clear progress state while Jira and the selected LLM are being called.
- Render generated test cases as Markdown in the assistant message.
- Provide a concise error message when the ticket key is missing, Jira fails, the template is missing, or both LLM routes fail.
- Provide a link or navigation affordance to the Settings page.

### Screen 2: Settings (`pages/settings.py`)

- Show Jira base URL and email as editable non-secret settings, if the chosen configuration model permits them to be overridden locally.
- Show masked Jira token and Groq key status; never render their values.
- Provide an Ollama/Groq provider selector with Ollama selected by default.
- Save the provider selection and any permitted non-secret settings to the local configuration store.
- Explain validation state without exposing secrets.
- Keep Ollama endpoint and model defaults fixed as:
  - Endpoint: `http://localhost:11434`
  - Model: `gemma3:1b`
- Do not download or pull the Ollama model.

## Module Responsibilities

### `config_store.py`

- Define the settings shape and default provider (`ollama`).
- Load `.env` values once and expose validated configuration to the rest of the app.
- Read and write the local non-secret settings file.
- Distinguish missing credentials from invalid provider/configuration values.
- Keep persistence details out of the UI and service clients.

### `jira_client.py`

- Accept the Jira base URL, email, and API token through dependency/configuration inputs.
- Parse and normalize the base URL without allowing credentials in the URL.
- Fetch one Jira issue by key using the Jira REST API and a request timeout.
- Extract summary, description, and acceptance criteria when available.
- Normalize Jira rich-text/ADF descriptions into readable text where required.
- Raise controlled, user-safe errors for authentication, authorization, not-found, timeout, and server failures.

### `llm_client.py`

- Build the final generation prompt from the local template and normalized Jira content.
- Call Ollama first when the provider is `ollama`, using the existing endpoint and `gemma3:1b` model.
- Call Groq directly only when the provider is `groq` or after an Ollama availability/request failure that qualifies for fallback.
- Require a configured Groq key before any Groq call.
- Set request timeouts, handle malformed/empty responses, and return a consistent generated-text result.
- Keep fallback behavior explicit so Groq is never contacted during a successful Ollama request.

### `templates/test_case_template.md`

- Define the output contract for test cases, including title, preconditions, test data, steps, expected results, priority, and coverage notes.
- Include placeholders for Jira key, summary, description, and acceptance criteria.
- Instruct the model not to invent unavailable requirements and to identify assumptions clearly.

### `app.py`

- Initialize configuration and session state.
- Parse Jira keys from user messages with a strict pattern such as `[A-Z][A-Z0-9]+-\\d+`.
- Orchestrate: parse key -> fetch Jira issue -> load template -> generate -> render.
- Keep UI code separate from Jira and LLM implementation details.

## End-to-End Data Flow

```text
User chat request
  -> extract Jira key
  -> load validated env/config values
  -> jira_client fetches issue
  -> normalize summary/description/acceptance criteria
  -> load templates/test_case_template.md
  -> llm_client merges ticket data into template
  -> Ollama (default)
       -> Groq only on explicit Groq selection or Ollama failure
  -> render generated Markdown in chat
```

## Build Sequence

1. Add the secret/config ignore rules and `.env.example`.
2. Add `requirements.txt` with pinned or minimum compatible versions for Streamlit, `python-dotenv`, `requests`, and the Groq client if used.
3. Implement `config_store.py` and verify environment loading, defaults, missing-secret handling, and provider persistence without printing values.
4. Implement `jira_client.py` with timeout-aware REST calls and response normalization.
5. Add the sample template and implement `llm_client.py`, including Ollama-first routing and narrowly scoped Groq fallback.
6. Implement `app.py` and `pages/settings.py` around the service modules.
7. Run focused checks after each module, then perform a local end-to-end smoke test with a real `.env` supplied by the user and a non-sensitive Jira ticket.

## Validation Checklist

- App starts with Ollama as the default provider.
- No Ollama model pull/download is attempted.
- A valid Jira key is extracted from a chat request.
- Jira summary, description, and acceptance criteria reach the generation prompt.
- A missing or malformed Jira key is rejected before an API call.
- Jira authentication, not-found, timeout, and server errors are surfaced safely.
- Successful Ollama generation does not invoke Groq.
- Ollama failure invokes Groq only when a Groq key is configured.
- Explicit Groq selection invokes Groq without first calling Ollama.
- Missing Groq configuration produces a clear error rather than a network call.
- Settings persist provider choice across Streamlit reruns.
- Tokens and API keys remain masked and absent from logs/output.
- `.env` and local configuration paths are ignored by Git.
- Generated test cases follow the template structure and preserve unknowns as assumptions.

## Definition of Done

The requested files exist, the two Streamlit screens are usable, the complete Jira-to-test-case flow works with the supplied `.env`, Ollama is the default path, Groq fallback rules are enforced, secrets are excluded from source control and UI output, and the validation checklist has been exercised with results recorded in the implementation notes or final change summary.