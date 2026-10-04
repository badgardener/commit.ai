import anthropic
from anthropic import Anthropic

from .error import AIError


def GetResponse(prompt: str, key: str) -> str:
    client = Anthropic(api_key=key)

    errors = []

    try:
        models = client.models.list()
    except Exception as e:
        raise AIError(f"Failed to retrieve Anthropic models: {e}") from e

    for model in models:
        try:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text or ""
        except anthropic.NotFoundError as e:
            errors.append(f"{model}: {e}")
        except anthropic.RateLimitError as e:
            errors.append(f"{model}: {e}")
        except anthropic.BadRequestError as e:
            errors.append(f"{model}: {e}")
        except anthropic.APIStatusError as e:
            errors.append(f"{model}: {e}")
        except Exception as e:  # noqa: BLE001
            errors.append(f"{model}: {e}")

    raise AIError("All available Anthropic models failed:\n" + "\n".join(errors))
