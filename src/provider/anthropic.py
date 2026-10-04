import anthropic
from anthropic import Anthropic

from .error import AIError


def GetResponse(prompt: str, key: str) -> str:
    client = Anthropic(api_key=key)

    if len(prompt.split()) < 20 and not any(
        k in prompt.lower() for k in ["analyze", "optimize", "complex", "code"]
    ):
        primary_model = "claude-3-5-haiku-latest"
        fallback_model = None
    else:
        primary_model = "claude-3-5-sonnet-latest"
        fallback_model = "claude-3-5-haiku-latest"

    try:
        response = client.messages.create(
            model=primary_model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text or ""  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportAttributeAccessIssue]
    except (anthropic.RateLimitError, anthropic.BadRequestError) as e:
        if fallback_model and (
            "insufficient_quota" in str(e) or "rate_limit" in str(e)
        ):
            try:
                response = client.messages.create(
                    model=fallback_model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text or ""  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportAttributeAccessIssue]
            except Exception as fallback_err:
                raise AIError(
                    f"Both primary and fallback models failed: {fallback_err}"
                ) from fallback_err

        raise AIError(f"Anthropic API error: {e}") from e
    except Exception as e:
        raise AIError(f"Anthropic completion failed: {e}") from e
