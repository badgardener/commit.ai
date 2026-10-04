from google import genai
from google.genai import errors

from .error import AIError


def GetResponse(prompt: str, key: str) -> str:
    client = genai.Client(api_key=key)

    if len(prompt.split()) < 20 and not any(
        k in prompt.lower() for k in ["analyze", "optimize", "complex", "code"]
    ):
        primary_model = "gemini-2.5-flash"
        fallback_model = None
    else:
        primary_model = "gemini-3.8-flash"
        fallback_model = "gemini-2.5-flash"

    try:
        response = client.models.generate_content(model=primary_model, contents=prompt)  # pyright: ignore[reportUnknownMemberType]
        return response.text or ""
    except errors.APIError as e:
        if fallback_model and (
            "429" in str(e) or "quota" in str(e).lower() or "limit" in str(e).lower()
        ):
            try:
                response = client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
                    model=fallback_model, contents=prompt
                )
                return response.text or ""
            except Exception as fallback_err:
                raise AIError(
                    f"Both primary and fallback models failed: {fallback_err}"
                ) from fallback_err

        raise AIError(f"Google GenAI API error: {e}") from e
    except Exception as e:
        raise AIError(f"Google GenAI completion failed: {e}") from e
