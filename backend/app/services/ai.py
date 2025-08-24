import os
from typing import Optional

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - library is optional
    OpenAI = None  # type: ignore

_client: Optional[OpenAI] = None

if OpenAI is not None and os.getenv("OPENAI_API_KEY"):
    _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(prompt: str) -> str:
    """Generate a response for the given prompt using an LLM.

    If the OpenAI client is available and an API key is configured, the
    prompt is sent to the model. Otherwise a simple echo fallback is
    returned.
    """
    if _client is None:
        return f"Echo: {prompt}"

    completion = _client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt,
    )
    return completion.output_text
