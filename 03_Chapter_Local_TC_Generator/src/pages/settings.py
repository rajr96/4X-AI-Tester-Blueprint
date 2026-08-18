"""Settings screen for provider selection and configuration status."""

import streamlit as st

from config_store import load_config, save_provider


st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("Settings")
config = load_config()

st.subheader("LLM provider")
provider = st.selectbox("Provider", ["ollama", "groq"], index=["ollama", "groq"].index(config.provider))
if st.button("Save provider"):
    save_provider(provider)
    st.success("Provider saved.")

st.subheader("Connection status")
st.write(f"Jira URL: `{config.jira_url or 'missing'}`")
st.write(f"Jira email configured: {'yes' if config.jira_email else 'no'}")
st.write(f"Jira API token configured: {'yes' if config.jira_api_token else 'no'}")
st.write(f"Groq API key configured: {'yes' if config.groq_api_key else 'no'}")
st.write(f"Ollama endpoint: `{config.ollama_url}`")
st.write(f"Ollama model: `{config.ollama_model}`")
st.info("Credentials are loaded from the local .env file and are never displayed or persisted by this screen.")