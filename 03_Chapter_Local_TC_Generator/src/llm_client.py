"""Ollama-first generation with controlled Groq fallback."""

from __future__ import annotations

from typing import Any

import requests

from config_store import AppConfig


class LLMError(RuntimeError):
    """An expected model request or response failure."""


def _request_ollama(config: AppConfig, prompt: str) -> str:
    response = requests.post(
        f"{config.ollama_url}/api/generate",
        json={"model": config.ollama_model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    response.raise_for_status()
    result: Any = response.json().get("response")
    if not result:
        raise LLMError("Ollama returned an empty response.")
    return str(result)


def _request_groq(config: AppConfig, prompt: str) -> str:
    if not config.groq_api_key:
        raise LLMError("Groq is selected, but GROQ_API_TOKEN is not configured.")
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {config.groq_api_key}"},
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=120,
    )
    response.raise_for_status()
    result: Any = response.json().get("choices", [{}])[0].get("message", {}).get("content")
    if not result:
        raise LLMError("Groq returned an empty response.")
    return str(result)


def generate(config: AppConfig, prompt: str) -> str:
    if config.provider == "groq":
        try:
            return _request_groq(config, prompt)
        except (requests.RequestException, ValueError, IndexError, KeyError) as exc:
            raise LLMError("Groq generation failed.") from exc

    try:
        return _request_ollama(config, prompt)
    except (requests.RequestException, ValueError, IndexError, KeyError, LLMError) as ollama_error:
        if not config.groq_api_key:
            raise LLMError("Ollama is unavailable and no Groq fallback key is configured.") from ollama_error
        try:
            return _request_groq(config, prompt)
        except (requests.RequestException, ValueError, IndexError, KeyError, LLMError) as groq_error:
            raise LLMError("Both Ollama and Groq generation failed.") from groq_error