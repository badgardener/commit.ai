import openai
from openai import OpenAI

from .error import AIError


def GetResponse(prompt: str, key: str) -> str:
    client = OpenAI(api_key=key)
    failures: list[str] = []

    try:
        models = client.models.list()
    except Exception as e:
        raise AIError(f"Failed to retrieve OpenAI models: {e}") from e

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

        except openai.RateLimitError as e:
            failures.append(f"{name}: rate limit: {e}")
        except openai.BadRequestError as e:
            failures.append(f"{name}: bad request: {e}")
        except openai.NotFoundError as e:
            failures.append(f"{name}: unavailable: {e}")
        except openai.APIError as e:
            failures.append(f"{name}: API error: {e}")
        except Exception as e:  # noqa: BLE001
            failures.append(f"{name}: {e}")

    raise AIError("All available OpenAI models failed:\n" + "\n".join(failures))
