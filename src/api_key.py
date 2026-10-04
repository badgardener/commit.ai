from typing import Literal

import keyring

APP = "Commit.AI"

ApiService = Literal[
    "openai_secret_key",
    "openrouter_secret_key",
    "genai_secret_key",
    "anthropic_secret_key",
    "groq_secret_key",
]

OPEN_AI_SERVICE = "openai_secret_key"
OPEN_ROUTER_SERVICE = "openrouter_secret_key"
GENAI_SERVICE = "genai_secret_key"
ANTHROPIC_SERVICE = "anthropic_secret_key"
GROQ_SERVICE = "groq_secret_key"


def HowManyKeys() -> int:
    return sum(
        keyring.get_password(APP, service) is not None
        for service in [
            OPEN_AI_SERVICE,
            OPEN_ROUTER_SERVICE,
            GENAI_SERVICE,
            ANTHROPIC_SERVICE,
            GROQ_SERVICE,
        ]
    )


def GetApiKey(service: ApiService) -> str | None:
    return keyring.get_password(APP, service)


def SetApiKey(
    service: ApiService,
    api: str,
) -> None:
    keyring.set_password(APP, service, api)


def DeleteApiKey(service: ApiService) -> None:
    GetApiKey(service) and keyring.delete_password(APP, service)  # pyright: ignore[reportUnusedExpression]
