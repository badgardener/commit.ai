from pathlib import Path
from typing import get_args

import anthropic
import rich
import rich.prompt
from google import genai
from groq import Groq
from openai import OpenAI
from rich import print as rprint

import ai
import api_key
import prompt

ProviderOptions = api_key.ApiService
ProviderOptionsList = get_args(ProviderOptions)

DRAGON_FG = "#C5C9C5"
DRAGON_BLUE = "#8BA4B0"
DRAGON_GREEN = "#8A9A7B"
DRAGON_YELLOW = "#C4B28A"
DRAGON_RED = "#C4746E"
DRAGON_PURPLE = "#A292A3"
DRAGON_ORANGE = "#B6927B"
DRAGON_MUTED = "#737C73"


def verify_api_key(key: str, provider: ProviderOptions) -> bool:
    try:
        match provider:
            case "anthropic":
                client = anthropic.Anthropic(api_key=key)
                client.models.list(limit=1)

            case "genai":
                client = genai.Client(api_key=key)
                next(iter(client.models.list(config={"page_size": 1})), None)

            case "groq":
                client = Groq(api_key=key)
                client.models.list()

            case "openai":
                client = OpenAI(api_key=key)
                client.models.list()

            case "openrouter":
                client = OpenAI(
                    api_key=key,
                    base_url="https://openrouter.ai/api/v1",
                )
                client.models.list()

        return True

    except Exception:  # noqa: BLE001
        return False


def print_help_provider(provider: ProviderOptions) -> None:
    match provider:
        case "anthropic":
            rprint(
                f"[bold {DRAGON_FG}]Anthropic API Key[/bold {DRAGON_FG}]\n"
                f"Get your API key from:\n"
                f"  [link=https://console.anthropic.com/settings/keys][{DRAGON_BLUE}]https://console.anthropic.com/settings/keys[/{DRAGON_BLUE}][/link]\n\n"
                f"[{DRAGON_MUTED}]1.[/{DRAGON_MUTED}] Sign in or create an Anthropic account.\n"
                f"[{DRAGON_MUTED}]2.[/{DRAGON_MUTED}] Open [bold {DRAGON_YELLOW}]API Keys[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]3.[/{DRAGON_MUTED}] Click [bold {DRAGON_YELLOW}]Create Key[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]4.[/{DRAGON_MUTED}] Copy the generated key and add it to Commit.AI."
            )

        case "genai":
            rprint(
                f"[bold {DRAGON_FG}]Google Gemini API Key[/bold {DRAGON_FG}]\n"
                f"Get your API key from:\n"
                f"  [link=https://aistudio.google.com/apikey][{DRAGON_BLUE}]https://aistudio.google.com/apikey[/{DRAGON_BLUE}][/link]\n\n"
                f"[{DRAGON_MUTED}]1.[/{DRAGON_MUTED}] Sign in with your Google account.\n"
                f"[{DRAGON_MUTED}]2.[/{DRAGON_MUTED}] Open [bold {DRAGON_YELLOW}]Get API key[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]3.[/{DRAGON_MUTED}] Create an API key.\n"
                f"[{DRAGON_MUTED}]4.[/{DRAGON_MUTED}] Copy the key and add it to Commit.AI."
            )

        case "groq":
            rprint(
                f"[bold {DRAGON_FG}]Groq API Key[/bold {DRAGON_FG}]\n"
                f"Get your API key from:\n"
                f"  [link=https://console.groq.com/keys][{DRAGON_BLUE}]https://console.groq.com/keys[/{DRAGON_BLUE}][/link]\n\n"
                f"[{DRAGON_MUTED}]1.[/{DRAGON_MUTED}] Sign in or create a Groq account.\n"
                f"[{DRAGON_MUTED}]2.[/{DRAGON_MUTED}] Open [bold {DRAGON_YELLOW}]API Keys[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]3.[/{DRAGON_MUTED}] Click [bold {DRAGON_YELLOW}]Create API Key[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]4.[/{DRAGON_MUTED}] Copy the key and add it to Commit.AI."
            )

        case "openai":
            rprint(
                f"[bold {DRAGON_FG}]OpenAI API Key[/bold {DRAGON_FG}]\n"
                f"Get your API key from:\n"
                f"  [link=https://platform.openai.com/api-keys][{DRAGON_BLUE}]https://platform.openai.com/api-keys[/{DRAGON_BLUE}][/link]\n\n"
                f"[{DRAGON_MUTED}]1.[/{DRAGON_MUTED}] Sign in or create an OpenAI account.\n"
                f"[{DRAGON_MUTED}]2.[/{DRAGON_MUTED}] Open [bold {DRAGON_YELLOW}]API Keys[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]3.[/{DRAGON_MUTED}] Click [bold {DRAGON_YELLOW}]Create new secret key[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]4.[/{DRAGON_MUTED}] Copy the key and add it to Commit.AI."
            )

        case "openrouter":
            rprint(
                f"[bold {DRAGON_FG}]OpenRouter API Key[/bold {DRAGON_FG}]\n"
                f"Get your API key from:\n"
                f"  [link=https://openrouter.ai/settings/keys][{DRAGON_BLUE}]https://openrouter.ai/settings/keys[/{DRAGON_BLUE}][/link]\n\n"
                f"[{DRAGON_MUTED}]1.[/{DRAGON_MUTED}] Sign in or create an OpenRouter account.\n"
                f"[{DRAGON_MUTED}]2.[/{DRAGON_MUTED}] Open [bold {DRAGON_YELLOW}]API Keys[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]3.[/{DRAGON_MUTED}] Click [bold {DRAGON_YELLOW}]Create Key[/bold {DRAGON_YELLOW}].\n"
                f"[{DRAGON_MUTED}]4.[/{DRAGON_MUTED}] Copy the key and add it to Commit.AI."
            )


def AddApi(provider: ProviderOptions) -> None:
    if api_key.GetApiKey(provider) and not rich.prompt.Confirm.ask(
        f"[{DRAGON_FG}]Key already exists. Overwrite?[/{DRAGON_FG}]"
    ):
        return

    print_help_provider(provider)

    key: str = rich.prompt.Prompt.ask(
        f"[{DRAGON_BLUE}]API KEY[/{DRAGON_BLUE}]",
        password=True,
    )

    if verify_api_key(key, provider):
        api_key.SetApiKey(provider, key)
        rprint(f"[{DRAGON_GREEN}]API key verified and saved.[/{DRAGON_GREEN}]")
    else:
        rprint(f"[{DRAGON_RED}]Invalid API key or provider unavailable.[/{DRAGON_RED}]")


def RemoveApi(provider: ProviderOptions) -> None:
    if not api_key.GetApiKey(provider):
        rprint(f"[{DRAGON_RED}]No key added to the app for {provider}.[/{DRAGON_RED}]")
        return

    if rich.prompt.Confirm.ask(f"[{DRAGON_FG}]Remove?[/{DRAGON_FG}]"):
        api_key.DeleteApiKey(provider)
        rprint(f"[{DRAGON_GREEN}]API key removed.[/{DRAGON_GREEN}]")


def ListApi() -> None:
    if api_key.HowManyKeys() == 0:
        rprint(f"[{DRAGON_RED}]No keys added to the app.[/{DRAGON_RED}]")
        return

    services = (
        (api_key.OPEN_AI_SERVICE, "OpenAI"),
        (api_key.OPEN_ROUTER_SERVICE, "OpenRouter"),
        (api_key.GENAI_SERVICE, "GenAI"),
        (api_key.GROQ_SERVICE, "Groq"),
        (api_key.ANTHROPIC_SERVICE, "Anthropic"),
    )

    for service, name in services:
        if api_key.GetApiKey(service):
            rprint(
                f"[{DRAGON_GREEN}]●[/{DRAGON_GREEN}] "
                f"[{DRAGON_FG}]{name} Service available.[/{DRAGON_FG}]"
            )


def Generate(path: Path, provider: ProviderOptions) -> None:
    if not (key := api_key.GetApiKey(provider)):
        rprint(f"[{DRAGON_RED}]No key added to the app for {provider}.[/{DRAGON_RED}]")
        return

    prmp: str = prompt.BuildFullPrompt(path)
    context: ai.AI = ai.AI(prmp)

    note_msg: str = (
        "Generating... NOTE: AI can give incorrect information. "
        "Always review the generated commit message before using it."
    )

    print(
        note_msg,
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

    print(
        f"\r{' ' * len(note_msg)}",
        end="",
        flush=True,
    )

    print(f"\r{response}")
