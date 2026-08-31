import json
import os
from typing import Any, Dict, Optional

import requests


class LLMClient:
    def __init__(
        self,
        provider: Optional[str] = None,
        ollama_url: Optional[str] = None,
        ollama_model: Optional[str] = None,
        groq_api_token: Optional[str] = None,
        groq_model: Optional[str] = None,
        timeout: int = 120,
    ):
        self.provider = (provider or os.getenv("LLM_PROVIDER") or "ollama").strip().lower()
        self.ollama_url = (ollama_url or os.getenv("OLLAMA_URL") or "http://localhost:11434").rstrip("/")
        self.ollama_model = ollama_model or os.getenv("OLLAMA_MODEL") or "gemma3:1b"
        self.groq_api_token = groq_api_token or os.getenv("GROQ_API_TOKEN") or os.getenv("GROQ_API_KEY") or ""
        self.groq_model = groq_model or os.getenv("GROQ_MODEL") or "openai/gpt-oss-20b"
        self.timeout = timeout

        if self.provider not in {"ollama", "groq"}:
            raise ValueError("Provider must be either 'ollama' or 'groq'.")

    def generate(self, prompt: str) -> Dict[str, Any]:
        if self.provider == "groq":
            raw = self._generate_via_groq(prompt)
        else:
            raw = self._generate_via_ollama(prompt)
        return self._parse_json_payload(raw)

    def _generate_via_ollama(self, prompt: str) -> str:
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0},
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        raw = payload.get("response")
        if not raw:
            raise RuntimeError("Ollama returned an empty response.")
        return str(raw)

    def _generate_via_groq(self, prompt: str) -> str:
        if not self.groq_api_token:
            raise RuntimeError("Groq is selected, but GROQ_API_TOKEN is not configured.")

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.groq_api_token}"},
            json={
                "model": self.groq_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        result = payload.get("choices", [{}])[0].get("message", {}).get("content")
        if not result:
            raise RuntimeError("Groq returned an empty response.")
        return str(result)

    @staticmethod
    def _parse_json_payload(raw: str) -> Dict[str, Any]:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            text = raw.strip()
            if text.startswith("```") and text.endswith("```"):
                text = text.strip("`\n")
                if text.lower().startswith("json"):
                    text = text[4:].lstrip()
                payload = json.loads(text)
            else:
                raise RuntimeError("The model response was not valid JSON.")

        if not isinstance(payload, dict):
            raise RuntimeError("The model response did not contain a JSON object.")
        return payload