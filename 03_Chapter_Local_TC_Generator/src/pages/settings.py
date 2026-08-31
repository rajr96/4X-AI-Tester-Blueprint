"""Settings screen for provider selection and configuration status."""

import streamlit as st

from config_store import load_config, save_provider

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 35%, #1d4ed8 100%);
    }
    div[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.78);
    }
    .stAlert, .stDataFrame {
        border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("Settings")
config = load_config()

with st.container():
    st.subheader("LLM provider")
    provider = st.selectbox(
        "Provider",
        ["ollama", "groq"],
        index=["ollama", "groq"].index(config.provider),
        help="Choose the model provider used for generation.",
    )
    if st.button("Save provider", type="primary"):
        save_provider(provider)
        st.success("Provider saved.")

st.subheader("Connection status")
status_columns = st.columns(2)
with status_columns[0]:
    st.markdown(f"**Jira URL:** `{config.jira_url or 'missing'}`")
    st.markdown(f"**Jira email configured:** {'yes' if config.jira_email else 'no'}")
    st.markdown(f"**Jira API token configured:** {'yes' if config.jira_api_token else 'no'}")
with status_columns[1]:
    st.markdown(f"**Groq API key configured:** {'yes' if config.groq_api_key else 'no'}")
    st.markdown(f"**Ollama endpoint:** `{config.ollama_url}`")
    st.markdown(f"**Ollama model:** `{config.ollama_model}`")

st.info("Credentials are loaded from the local .env file and are never displayed or persisted by this screen.")