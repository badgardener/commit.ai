import groq
from groq import Groq

from .error import AIError


def GetResponse(prompt: str, key: str) -> str:
    client = Groq(api_key=key)
    failures: list[str] = []

    try:
        models = client.models.list()
    except Exception as e:
        raise AIError(f"Failed to retrieve Groq models: {e}") from e

    for model in models.data:
        name = getattr(model, "id", None)

        if not name:
            continue

        try:
            response = client.chat.completions.create(
                model=name,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.choices[0].message.content
            if content:
                return content

            failures.append(f"{name}: empty response")

        except groq.RateLimitError as e:
            failures.append(f"{name}: rate limit: {e}")
        except groq.BadRequestError as e:
            failures.append(f"{name}: bad request: {e}")
        except groq.APIError as e:
            failures.append(f"{name}: API error: {e}")
        except Exception as e:  # noqa: BLE001
            failures.append(f"{name}: {e}")

    raise AIError("All available Groq models failed:\n" + "\n".join(failures))
