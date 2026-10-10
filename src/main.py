import os
import platform
import sys
from pathlib import Path

import rich
from rich.console import Console

import core
import prompt
from core import (
    DRAGON_BLUE,
    DRAGON_FG,
    DRAGON_GREEN,
    DRAGON_MUTED,
    DRAGON_ORANGE,
    DRAGON_PURPLE,
    DRAGON_RED,
    DRAGON_YELLOW,
)

VERSION = "26.1.2"

console = Console()


def print_help() -> None:
    console.print(
        f"\n[bold {DRAGON_FG}]Usage:[/bold {DRAGON_FG}] "
        f"[bold {DRAGON_YELLOW}]commit.ai[/bold {DRAGON_YELLOW}] "
        f"[{DRAGON_BLUE}]<command> [arguments][/{DRAGON_BLUE}]\n\n"
        f"[bold {DRAGON_PURPLE}]Options:[/bold {DRAGON_PURPLE}]\n"
        f"  [{DRAGON_GREEN}]-h, --help[/{DRAGON_GREEN}]          Show this help message and exit.\n"
        f"  [{DRAGON_GREEN}]-v, --version[/{DRAGON_GREEN}]       Show the Commit.AI version and exit.\n\n"
        f"[bold {DRAGON_PURPLE}]Commands:[/bold {DRAGON_PURPLE}]\n"
        f"  [{DRAGON_GREEN}]add-api[/{DRAGON_GREEN}]            Add or update an API key for an AI provider.\n"
        f"  [{DRAGON_GREEN}]remove-api[/{DRAGON_GREEN}]         Remove a stored API key.\n"
        f"  [{DRAGON_GREEN}]list-api[/{DRAGON_GREEN}]           List configured AI providers.\n"
        f"  [{DRAGON_GREEN}]generate[/{DRAGON_GREEN}]           Generate a Git commit message from repository changes.\n"
        f"  [{DRAGON_GREEN}]generate-prompt[/{DRAGON_GREEN}]    Generate and display the full prompt for a repository.\n"
        f"\n[bold {DRAGON_PURPLE}]Style:[/bold {DRAGON_PURPLE}]\n"
        f"  [{DRAGON_GREEN}]--style <style>[/{DRAGON_GREEN}]  Add a custom style instruction to the generated prompt.\n"
    )


def print_command_help(command: str) -> None:
    if command == "add-api":
        console.print(
            f"\n[bold {DRAGON_FG}]Usage:[/bold {DRAGON_FG}] "
            f"[bold {DRAGON_YELLOW}]Commit.AI add-api[/bold {DRAGON_YELLOW}] "
            f"[{DRAGON_BLUE}]<provider>[/{DRAGON_BLUE}]\n\n"
            f"[{DRAGON_FG}]Add or update an API key for an AI provider.[/{DRAGON_FG}]\n\n"
            f"[bold {DRAGON_PURPLE}]Arguments:[/bold {DRAGON_PURPLE}]\n"
            f"  [{DRAGON_GREEN}]<provider>[/{DRAGON_GREEN}]       AI provider to configure.\n"
        )

    elif command == "remove-api":
        console.print(
            f"\n[bold {DRAGON_FG}]Usage:[/bold {DRAGON_FG}] "
            f"[bold {DRAGON_YELLOW}]Commit.AI remove-api[/bold {DRAGON_YELLOW}] "
            f"[{DRAGON_BLUE}]<provider>[/{DRAGON_BLUE}]\n\n"
            f"[{DRAGON_FG}]Remove a stored API key.[/{DRAGON_FG}]\n\n"
            f"[bold {DRAGON_PURPLE}]Arguments:[/bold {DRAGON_PURPLE}]\n"
            f"  [{DRAGON_GREEN}]<provider>[/{DRAGON_GREEN}]       AI provider whose API key should be removed.\n"
        )

    elif command == "list-api":
        console.print(
            f"\n[bold {DRAGON_FG}]Usage:[/bold {DRAGON_FG}] "
            f"[bold {DRAGON_YELLOW}]Commit.AI list-api[/bold {DRAGON_YELLOW}]\n\n"
            f"[{DRAGON_FG}]List configured AI providers.[/{DRAGON_FG}]\n"
        )

    elif command == "generate":
        console.print(
            f"\n[bold {DRAGON_FG}]Usage:[/bold {DRAGON_FG}] "
            f"[bold {DRAGON_YELLOW}]Commit.AI generate[/bold {DRAGON_YELLOW}] "
            f"[{DRAGON_BLUE}]<provider> [path] [--style <request>][/{DRAGON_BLUE}]\n\n"
            f"[{DRAGON_FG}]Generate a Git commit message from repository changes.[/{DRAGON_FG}]\n\n"
            f"[bold {DRAGON_PURPLE}]Arguments:[/bold {DRAGON_PURPLE}]\n"
            f"  [{DRAGON_GREEN}]<provider>[/{DRAGON_GREEN}]        AI provider to use for commit message generation.\n"
            f"  [{DRAGON_GREEN}][path][/{DRAGON_GREEN}]            Path to the Git repository. "
            f"[{DRAGON_MUTED}][default: .][/{DRAGON_MUTED}]\n"
            f"  [{DRAGON_GREEN}]--style <style>[/{DRAGON_GREEN}]  Add a custom style instruction to the prompt before generation.\n"
        )

    elif command == "generate-prompt":
        console.print(
            f"\n[bold {DRAGON_FG}]Usage:[/bold {DRAGON_FG}] "
            f"[bold {DRAGON_YELLOW}]Commit.AI generate-prompt[/bold {DRAGON_YELLOW}] "
            f"[{DRAGON_BLUE}][path] [--style <request>][/{DRAGON_BLUE}]\n\n"
            f"[{DRAGON_FG}]Generate and display the full AI prompt for a repository without calling an AI provider.[/{DRAGON_FG}]\n\n"
            f"[bold {DRAGON_PURPLE}]Arguments:[/bold {DRAGON_PURPLE}]\n"
            f"  [{DRAGON_GREEN}][path][/{DRAGON_GREEN}]            Path to the Git repository. "
            f"[{DRAGON_MUTED}][default: .][/{DRAGON_MUTED}]\n"
            f"  [{DRAGON_GREEN}]--style <style>[/{DRAGON_GREEN}]  Add a custom style instruction to the generated prompt.\n"
        )


def validate_provider(provider_str: str) -> None:
    if provider_str in core.ProviderOptionsList:
        return

    valid_options = ", ".join(core.ProviderOptionsList)
    raise ValueError(f"Invalid provider '{provider_str}'. Choose from: {valid_options}")


def parse_optional_request(
    args: list[str], *, command: str
) -> tuple[str | None, list[str]]:
    request: str | None = None
    remaining: list[str] = []
    index = 0

    while index < len(args):
        token = args[index]

        if token in ("-h", "--help"):
            print_command_help(command)
            sys.exit(0)

        if token == "--style":
            if index + 1 >= len(args):
                raise ValueError("Missing value for style.")
            request = args[index + 1]
            index += 2
            continue

        if token.startswith("-"):
            raise ValueError(
                f"Unknown option: '{token}'. Use --help to list available options."
            )

        remaining.append(token)
        index += 1

    return request, remaining


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print_help()
        sys.exit(0)

    if args[0] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    if args[0] in ("-v", "--version"):
        rich.print(
            f"[{DRAGON_MUTED}]Commit.AI[/{DRAGON_MUTED}] "
            f"[{DRAGON_BLUE}]{VERSION}[/{DRAGON_BLUE}]"
        )
        sys.exit(0)

    command = args[0]

    if command == "add-api":
        if len(args) > 1 and args[1] in ("-h", "--help"):
            print_command_help(command)
            sys.exit(0)

        if len(args) < 2:
            raise ValueError("Missing required argument: <provider>")

        provider = args[1]
        validate_provider(provider)
        core.AddApi(provider)  # type: ignore

    elif command == "remove-api":
        if len(args) > 1 and args[1] in ("-h", "--help"):
            print_command_help(command)
            sys.exit(0)

        if len(args) < 2:
            raise ValueError("Missing required argument: <provider>")

        provider = args[1]
        validate_provider(provider)
        core.RemoveApi(provider)  # type: ignore

    elif command == "list-api":
        if len(args) > 1 and args[1] in ("-h", "--help"):
            print_command_help(command)
            sys.exit(0)

        core.ListApi()

    elif command == "generate":
        if len(args) < 2:
            raise ValueError("Missing required argument: <provider>")

        provider = args[1]
        validate_provider(provider)

        request, remaining = parse_optional_request(args[2:], command=command)
        path_str = remaining[0] if remaining else "."
        path = Path(path_str).resolve()

        if len(remaining) > 1:
            raise ValueError(
                f"Unknown option: '{remaining[1]}'. Use --help to list available options."
            )

        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path_str}")

        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path_str}")

        if not os.access(path, os.R_OK):
            raise PermissionError(f"Path is not readable: {path_str}")

        core.Generate(path, provider, request)  # type: ignore

    elif command == "generate-prompt":
        request, remaining = parse_optional_request(args[1:], command=command)
        path_str = remaining[0] if remaining else "."
        path = Path(path_str).resolve()

        if len(remaining) > 1:
            raise ValueError(
                f"Unknown option: '{remaining[1]}'. Use --help to list available options."
            )

        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path_str}")

        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path_str}")

        if not os.access(path, os.R_OK):
            raise PermissionError(f"Path is not readable: {path_str}")

        prmpt = prompt.BuildFullPrompt(path, request)
        print(prmpt)

    else:
        raise ValueError(
            f"Unknown command: '{command}'. Use --help to list available commands."
        )


if __name__ == "__main__":
    try:
        if platform.system() == "Windows":
            os.system("")  # type: ignore

        main()
    except Exception as e:  # noqa: BLE001
        console.print(
            f"\n[bold {DRAGON_RED}]Error:[/bold {DRAGON_RED}] "
            f"[{DRAGON_ORANGE}]{e}[/{DRAGON_ORANGE}]"
        )
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        console.print(f"\n[bold {DRAGON_RED}]Exiting...[/bold {DRAGON_RED}] ")
        sys.exit(1)
