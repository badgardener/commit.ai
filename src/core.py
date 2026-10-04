from pathlib import Path
from typing import get_args

import rich
import rich.prompt
from rich import print

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
        print(f"[red]No key added to the app for {provider}.[/red]")
        return

    if rich.prompt.Confirm.ask("Remove?"):
        api_key.DeleteApiKey(provider)


def ListApi() -> None:
    if api_key.HowManyKeys() == 0:
        print("[red]No keys added to the app.[/red]")
        return

    api_key.GetApiKey(api_key.OPEN_AI_SERVICE) and print(
        "[green]OpenAI Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]

    api_key.GetApiKey(api_key.OPEN_ROUTER_SERVICE) and print(
        "[green]Open Router Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]

    api_key.GetApiKey(api_key.GENAI_SERVICE) and print(
        "[green]GenAI Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]

    api_key.GetApiKey(api_key.GROQ_SERVICE) and print(
        "[green]Groq Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]

    api_key.GetApiKey(api_key.ANTHROPIC_SERVICE) and print(
        "[green]Anthropic Service available.[/green]"
    )  # pyright: ignore[reportUnusedExpression]


def Generate(path: Path, provider: ProviderOptions) -> None:
    if not (key := api_key.GetApiKey(provider)):
        print(f"[red]No key added to the app for {provider}.[/red]")
        return

    prmp: str = prompt.BuildFullPrompt(
        prompt.GetRawPrompt(path), prompt.GetDirectionPrompt()
    )
    context: ai.AI = ai.AI(prmp)

    match provider:
        case "openai":
            print(context.GetFromOpenAI(key))

        case "anthropic":
            print(context.GetFromAnthropic(key))

        case "genai":
            print(context.GetFromGenAI(key))

        case "groq":
            print(context.GetFromGroq(key))

        case "openrouter":
            print(context.GetFromOpenRouter(key))
