from pathlib import Path
from typing import get_args

import rich
import rich.prompt
from rich import print as rprint

import ai
import api_key
import prompt

ProviderOptions = api_key.ApiService
ProviderOptionsList = get_args(ProviderOptions)


def AddApi(provider: ProviderOptions) -> None:
    if api_key.GetApiKey(provider) and not rich.prompt.Confirm.ask(
        "Key already exists. Overwrite?"
    ):
        return

    key: str = rich.prompt.Prompt.ask("API KEY", password=True)
    api_key.SetApiKey(provider, key)


def RemoveApi(provider: ProviderOptions) -> None:
    if not api_key.GetApiKey(provider):
        rprint(f"[red]No key added to the app for {provider}.[/red]")
        return

    if rich.prompt.Confirm.ask("Remove?"):
        api_key.DeleteApiKey(provider)


def ListApi() -> None:
    if api_key.HowManyKeys() == 0:
        rprint("[red]No keys added to the app.[/red]")
        return

    api_key.GetApiKey(api_key.OPEN_AI_SERVICE) and rprint(
        "[green]OpenAI Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]

    api_key.GetApiKey(api_key.OPEN_ROUTER_SERVICE) and rprint(
        "[green]Open Router Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]

    api_key.GetApiKey(api_key.GENAI_SERVICE) and rprint(
        "[green]GenAI Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]

    api_key.GetApiKey(api_key.GROQ_SERVICE) and rprint(
        "[green]Groq Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]

    api_key.GetApiKey(api_key.ANTHROPIC_SERVICE) and rprint(
        "[green]Anthropic Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]


def Generate(path: Path, provider: ProviderOptions) -> None:
    if not (key := api_key.GetApiKey(provider)):
        rprint(f"[red]No key added to the app for {provider}.[/red]")
        return

    prmp: str = prompt.BuildFullPrompt(path)
    context: ai.AI = ai.AI(prmp)

    print(
        "NOTE: AI CAN GIVE INCORRECT OR INCOMPLETE INFORMATION."
        " ALWAYS REVIEW THE GENERATED COMMIT MESSAGE BEFORE USING IT.",
        end="",
        flush=True,
    )

    match provider:
        case "openai":
            response = context.GetFromOpenAI(key)
        case "anthropic":
            response = context.GetFromAnthropic(key)
        case "genai":
            response = context.GetFromGenAI(key)
        case "groq":
            response = context.GetFromGroq(key)
        case "openrouter":
            response = context.GetFromOpenRouter(key)

    print(f"\r\033[2K{response}")
