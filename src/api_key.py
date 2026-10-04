from typing import Literal

import keyring

APP = "Commit.AI"

ApiService = Literal[
    "openai",
    "openrouter",
    "groq",
    "genai",
    "anthropic",
]

OPEN_AI_SERVICE = "openai"
OPEN_ROUTER_SERVICE = "openrouter"
GENAI_SERVICE = "genai"
ANTHROPIC_SERVICE = "anthropic"
GROQ_SERVICE = "groq"


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
