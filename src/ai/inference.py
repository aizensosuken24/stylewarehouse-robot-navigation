"""
AI inference helper module.

Provides a small, optional abstraction to call a local Ollama instance
or a remote AI service using a BYOK-style token. This file keeps
dependencies optional and uses `requests` only when the remote backend
is selected.

Usage:
    from src.ai.inference import generate_text
    text = generate_text("Summarise this", backend="local")

Configuration:
 - Local Ollama: runs an HTTP API on localhost (default: http://localhost:11434).
 - Remote: set environment variable `REMOTE_AI_URL` to the API endpoint.
 - BYOK token: set `AI_BEARER_TOKEN` or pass `token` argument.
"""
from __future__ import annotations
import os
from typing import Optional


def _call_local_ollama(prompt: str, model: str = "ollama", host: str = "http://localhost:11434") -> str:
    """Call a local Ollama-like HTTP API. Returns text or raises RuntimeError."""
    try:
        import requests
    except Exception as e:  # pragma: no cover - optional dependency
        raise RuntimeError("requests library is required for local inference calls") from e

    url = f"{host}/api/generate"
    payload = {"model": model, "prompt": prompt}
    resp = requests.post(url, json=payload, timeout=15)
    if not resp.ok:
        raise RuntimeError(f"Local inference failed: {resp.status_code} {resp.text}")
    data = resp.json()
    # Ollama-like responses sometimes use `text` or `response`
    return data.get("text") or data.get("response") or ""


def _call_remote_api(prompt: str, url: str, token: Optional[str] = None) -> str:
    """Call a remote AI endpoint with optional bearer token."""
    try:
        import requests
    except Exception as e:  # pragma: no cover
        raise RuntimeError("requests library is required for remote inference calls") from e

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = {"prompt": prompt}
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    if not resp.ok:
        raise RuntimeError(f"Remote inference failed: {resp.status_code} {resp.text}")
    data = resp.json()
    return data.get("text") or data.get("response") or ""


def get_env_token() -> Optional[str]:
    """Return token from environment if available (BYOK)."""
    return os.environ.get("AI_BEARER_TOKEN") or os.environ.get("BYOK_TOKEN")


def generate_text(
    prompt: str,
    backend: str = "local",
    model: str = "ollama",
    token: Optional[str] = None,
    remote_url: Optional[str] = None,
) -> str:
    """Generate text using the selected backend.

    backend: 'local' or 'remote'
    token: optional bearer token for remote backends (BYOK)
    remote_url: optional custom URL for remote backend; can also be set via REMOTE_AI_URL env var
    """
    token = token or get_env_token()
    if backend == "local":
        # Best-effort call to local Ollama API
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        return _call_local_ollama(prompt=prompt, model=model, host=host)

    if backend == "remote":
        url = remote_url or os.environ.get("REMOTE_AI_URL")
        if not url:
            raise RuntimeError("REMOTE_AI_URL must be set for remote backend")
        return _call_remote_api(prompt=prompt, url=url, token=token)

    raise ValueError("Unknown backend; choose 'local' or 'remote'")
