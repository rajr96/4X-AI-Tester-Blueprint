"""Ollama-first generation with controlled Groq fallback."""

from __future__ import annotations

import json
from typing import Any

import requests

from config_store import AppConfig


class LLMError(RuntimeError):
    """An expected model request or response failure."""


def validate_generation_json(raw_response: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise LLMError("The model response was not valid JSON.") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("scenario_coverage"), list):
        raise LLMError("The model response does not match the required JSON structure.")

    total_cases = 0
    applicable_categories = 0
    for category in payload["scenario_coverage"]:
        if not isinstance(category, dict) or not isinstance(category.get("scenario"), str):
            raise LLMError("A scenario entry is missing its name.")
        cases = category.get("test_cases", [])
        if category.get("applicable") is True:
            applicable_categories += 1
            if not isinstance(cases, list) or not 2 <= len(cases) <= 5:
                raise LLMError(f"Scenario '{category['scenario']}' must contain 2 to 5 test cases.")
            for case in cases:
                if not isinstance(case, dict) or not all(case.get(field) for field in ("id", "title", "steps", "expected_result")):
                    raise LLMError(f"Scenario '{category['scenario']}' contains an incomplete test case.")
            total_cases += len(cases)
        elif cases:
            raise LLMError(f"Not-applicable scenario '{category['scenario']}' must not contain test cases.")

    if not applicable_categories or not 2 <= total_cases <= 70:
        raise LLMError("The generated response must contain 2 to 70 test cases across applicable scenarios.")
    return payload


def _request_ollama(config: AppConfig, prompt: str) -> str:
    response = requests.post(
        f"{config.ollama_url}/api/generate",
        json={"model": config.ollama_model, "prompt": prompt, "stream": False, "format": "json", "options": {"temperature": 0}},
        timeout=120,
    )
    response.raise_for_status()
    result: Any = response.json().get("response")
    if not result:
        raise LLMError("Ollama returned an empty response.")
    validate_generation_json(str(result))
    return str(result)


def _request_groq(config: AppConfig, prompt: str) -> str:
    if not config.groq_api_key:
        raise LLMError("Groq is selected, but GROQ_API_TOKEN is not configured.")
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {config.groq_api_key}"},
        json={
            "model": config.groq_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        },
        timeout=120,
    )
    if response.status_code in {401, 403}:
        raise LLMError("Groq rejected the configured API key. Check GROQ_API_TOKEN.")
    if response.status_code == 404:
        raise LLMError(
            f"Groq model '{config.groq_model}' is unavailable or the key is invalid. "
            "Update GROQ_MODEL and verify GROQ_API_TOKEN."
        )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise LLMError(f"Groq request failed with status {response.status_code}: {response.text[:200]}") from exc
    result: Any = response.json().get("choices", [{}])[0].get("message", {}).get("content")
    if not result:
        raise LLMError("Groq returned an empty response.")
    validate_generation_json(str(result))
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
            raise LLMError(
                f"Both Ollama and Groq generation failed. Ollama: {ollama_error} Groq: {groq_error}"
            ) from groq_error