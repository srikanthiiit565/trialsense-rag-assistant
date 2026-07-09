"""Minimal Groq client wrapper.

This wrapper prefers the official `groq` package when available. If the
package is not installed, it raises a clear error instructing how to
install it. The wrapper provides an `invoke(prompt)` method returning an
object with a `.content` attribute to match the interface used by nodes.
"""
from types import SimpleNamespace

try:
    import groq
except Exception:
    groq = None


class GroqClient:
    def __init__(self, api_key: str, model: str, base_url: str | None = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        if groq is not None:
            # Attempt to construct the official client if available
            try:
                self.client = groq.Client(api_key=api_key)
            except Exception:
                self.client = None
        else:
            self.client = None

    def invoke(self, prompt: str) -> SimpleNamespace:
        if self.client is None:
            raise RuntimeError(
                "groq package not available; install with `pip install groq`"
            )

        # The official SDK may expose different methods; try common patterns
        # and raise a helpful error if the call fails.
        try:
            # Hypothetical modern API: client.generate(model=..., prompt=...)
            result = self.client.generate(model=self.model, prompt=prompt)
            # Try to extract text/content in a few common locations
            content = getattr(result, "text", None) or getattr(result, "content", None)
            if content is None:
                # Fallback to string conversion
                content = str(result)
            return SimpleNamespace(content=content)
        except Exception as exc:
            raise RuntimeError(f"Groq client invocation failed: {exc}")
