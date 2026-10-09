from google import genai
from google.genai import errors

from .error import AIError


def GetResponse(prompt: str, key: str) -> str:
    client = genai.Client(api_key=key)
    failures: list[str] = []

    try:
        models = list(client.models.list())
    except Exception as e:
        raise AIError(f"Failed to retrieve Google GenAI models: {e}") from e

    for model in models:
        name = getattr(model, "name", None)

        if not name or "generateContent" not in (
            getattr(model, "supported_actions", None) or []
        ):
            continue

        try:
            response = client.models.generate_content(  # type: ignore
                model=name,
                contents=prompt,
            )

            text = response.text
            if text:
                return text

            failures.append(f"{name}: empty response")

        except errors.APIError as e:
            failures.append(f"{name}: {e}")
        except Exception as e:  # noqa: BLE001
            failures.append(f"{name}: {e}")

    raise AIError("All available Google GenAI models failed:\n" + "\n".join(failures))
