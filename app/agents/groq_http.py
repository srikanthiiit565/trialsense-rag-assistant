"""Raw HTTP Groq client.

This client uses `httpx` to call the Groq Cloud HTTP API. The exact
endpoints and payloads vary between providers and over time; this implementation
tries a few common patterns and returns a SimpleNamespace with a `.content`
attribute for compatibility with existing code.

Adjust `GROQ_BASE_URL` and `GROQ_MODEL` in `.env` per Groq documentation.
"""
from types import SimpleNamespace
import json
import logging
import os
import random
import time

try:
    import httpx
except Exception:
    httpx = None


class GroqHTTPClient:
    def __init__(self, api_key: str, model: str, base_url: str | None = None, timeout: int = 30):
        if httpx is None:
            raise RuntimeError("httpx is required for GroqHTTPClient. Install with `pip install httpx[http2]`")
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/") if base_url else "https://api.groq.ai"
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def invoke(self, prompt: str) -> SimpleNamespace:
        """Try to call a Groq-like generate endpoint and return a `.content` response.

        This tries a couple of plausible endpoints; adapt to your provider's
        official API if these do not match.
        """
        # Candidate endpoints (may need adjustment)
        candidates = [
            f"{self.base_url}/v1/generate",
            f"{self.base_url}/v1/models/{self.model}/generate",
            f"{self.base_url}/v1/models/{self.model}:predict",
            f"{self.base_url}/v1/completions",
        ]

        payload = {
            "model": self.model,
            "prompt": prompt,
            # Groq Cloud may accept other keys like `max_tokens`, `temperature`, etc.
        }

        last_exc = None
        attempts = 3
        for url in candidates:
            backoff = 1.0
            for attempt in range(attempts):
                # Test hook for simulating failure in tests
                if os.getenv("GROQ_FORCE_FAIL"):
                    raise RuntimeError("Forced Groq failure (GROQ_FORCE_FAIL=1)")

                try:
                    resp = httpx.post(url, headers=self.headers, json=payload, timeout=self.timeout)
                    resp.raise_for_status()
                    data = resp.json()
                    # Try common locations for generated text
                    content = None
                    if isinstance(data, dict):
                        # Common fields
                        content = data.get("text") or data.get("content")
                        if not content:
                            # nested candidates
                            if "output" in data:
                                out = data["output"]
                                if isinstance(out, list) and len(out) > 0:
                                    # try first element
                                    content = out[0].get("text") if isinstance(out[0], dict) else str(out[0])
                            if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                                item = data["data"][0]
                                if isinstance(item, dict):
                                    content = item.get("text") or item.get("content") or json.dumps(item)
                    if content is None:
                        # fallback to raw text
                        content = resp.text
                    return SimpleNamespace(content=content)
                except Exception as exc:
                    last_exc = exc
                    logging.getLogger(__name__).debug("Groq request to %s failed (attempt %s/%s): %s", url, attempt + 1, attempts, exc)
                    # exponential backoff with jitter
                    time.sleep(backoff + random.random() * 0.1)
                    backoff *= 2
                    continue

        raise RuntimeError(f"Groq HTTP invocation failed for all candidate endpoints. Last error: {last_exc}")
