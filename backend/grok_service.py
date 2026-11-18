import json
import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
_client = httpx.Client(timeout=httpx.Timeout(35.0, connect=8.0), limits=httpx.Limits(max_connections=20, max_keepalive_connections=10))


class GroqServiceError(Exception):
    pass


def chat(system_prompt: str, user_prompt: str) -> str:
    if not GROQ_API_KEY:
        raise GroqServiceError("GROQ_API_KEY is not configured.")
    try:
        response = _client.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                "temperature": 0.25,
                "max_tokens": 1200,
                "response_format": {"type": "json_object"},
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as exc:
        raise GroqServiceError(f"AI service returned {exc.response.status_code}.")
    except (httpx.RequestError, KeyError, IndexError, json.JSONDecodeError) as exc:
        raise GroqServiceError("AI service is temporarily unavailable.") from exc
