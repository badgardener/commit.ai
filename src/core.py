from pathlib import Path
from typing import Literal

ProviderOptions = Literal[
    "openai",
    "openrouter",
    "groq",
    "genai",
    "anthropic",
]


def AddApi(provider: ProviderOptions) -> None: ...


def RemoveApi(provider: ProviderOptions) -> None: ...


def ListApi() -> None: ...


def Generate(path: Path, provider: ProviderOptions) -> None: ...
