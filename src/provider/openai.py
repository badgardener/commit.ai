import openai
from openai import OpenAI

from .error import AIError


def GetResponse(prompt: str, key: str) -> str:
    client = OpenAI(api_key=key)

    if len(prompt.split()) < 20 and not any(
        k in prompt.lower() for k in ["analyze", "optimize", "complex", "code"]
    ):
        primary_model = "gpt-4o-mini"
        fallback_model = None
    else:
        primary_model = "gpt-4o"
        fallback_model = "gpt-4o-mini"

    try:
        response = client.chat.completions.create(
            model=primary_model, messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content or ""
    except (openai.RateLimitError, openai.BadRequestError) as e:
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

        raise AIError(f"OpenAI API error: {e}") from e
    except Exception as e:
        raise AIError(f"OpenAI completion failed: {e}") from e
