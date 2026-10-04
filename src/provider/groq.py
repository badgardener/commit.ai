import groq
from groq import Groq

from .error import AIError


def GetResponse(prompt: str, key: str) -> str:
    client = Groq(api_key=key)

    if len(prompt.split()) < 20 and not any(
        k in prompt.lower() for k in ["analyze", "optimize", "complex", "code"]
    ):
        primary_model = "openai/gpt-oss-20b"
        fallback_model = None
    else:
        primary_model = "openai/gpt-oss-120b"
        fallback_model = "openai/gpt-oss-20b"

    try:
        response = client.chat.completions.create(
            model=primary_model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content or ""
    except (groq.RateLimitError, groq.BadRequestError) as e:
        if fallback_model and (
            "insufficient_quota" in str(e) or "rate_limit" in str(e)
        ):
            try:
                response = client.chat.completions.create(
                    model=fallback_model, messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content or ""
            except Exception as fallback_err:
                raise AIError(
                    f"Both primary and fallback models failed: {fallback_err}"
                ) from fallback_err

        raise AIError(f"Groq API error: {e}") from e
    except Exception as e:
        raise AIError(f"Groq completion failed: {e}") from e
