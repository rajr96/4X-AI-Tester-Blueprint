"""Environment and non-secret application settings."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "gemma3:1b"
DEFAULT_PROVIDER = "ollama"
SETTINGS_PATH = Path(__file__).resolve().parent / ".config" / "settings.json"


@dataclass(frozen=True)
class AppConfig:
    jira_url: str
    jira_email: str
    jira_api_token: str
    ollama_url: str
    ollama_model: str
    groq_api_key: str
    provider: str

    @property
    def has_jira_credentials(self) -> bool:
        return bool(self.jira_url and self.jira_email and self.jira_api_token)

    @property
    def has_groq_credentials(self) -> bool:
        return bool(self.groq_api_key)


def _read_local_settings() -> dict[str, str]:
    if not SETTINGS_PATH.exists():
        return {}
    try:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _normalize_jira_url(value: str) -> str:
    value = value.strip()
    if value.startswith("[") and "](" in value:
        value = value.split("](", 1)[1].rstrip(") ")
    if value and not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value.rstrip("/")


def _load_supplied_env_values(env_path: Path) -> None:
    """Accept the numbered KEY=value format currently present in the local file."""
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*(?:\d+\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if match:
            key, value = match.groups()
            os.environ[key] = value.strip().strip('"').strip("'")


def load_config() -> AppConfig:
    env_path = Path(__file__).resolve().parent / ".env"
    _load_supplied_env_values(env_path)
    local_settings = _read_local_settings()
    provider = local_settings.get("provider", DEFAULT_PROVIDER).lower()
    if provider not in {"ollama", "groq"}:
        provider = DEFAULT_PROVIDER

    return AppConfig(
        jira_url=_normalize_jira_url(os.getenv("JIRA_URL", os.getenv("JIRA_BASE_URL", ""))),
        jira_email=os.getenv("JIRA_EMAIL", "").strip(),
        jira_api_token=os.getenv("JIRA_API_TOKEN", "").strip(),
        ollama_url=os.getenv("OLLAMA_URL", DEFAULT_OLLAMA_URL).strip().rstrip("/"),
        ollama_model=os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL).strip(),
        groq_api_key=os.getenv("GROQ_API_TOKEN", os.getenv("GROQ_API_KEY", "")).strip(),
        provider=provider,
    )


def save_provider(provider: str) -> None:
    provider = provider.lower()
    if provider not in {"ollama", "groq"}:
        raise ValueError("Provider must be ollama or groq.")
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(
        json.dumps({"provider": provider}, indent=2) + "\n", encoding="utf-8"
    )