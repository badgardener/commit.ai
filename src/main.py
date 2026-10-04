import sys
from pathlib import Path

import rich
from rich.console import Console

VERSION = "26.0.0"

console = Console()

import core


def print_help() -> None:
    help_text = (
        "\n[bold cyan]Usage:[/bold cyan] [bold green]Commit.AI[/bold green] [cyan]<command> [arguments][/cyan]\n\n"
        "[bold white]Generate Git commit messages using AI.[/bold white]\n\n"
        "[bold magenta]Options:[/bold magenta]\n"
        "  [green]-h, --help[/green]          Show this help message and exit.\n"
        "  [green]-v, --version[/green]       Show the Commit.AI version and exit.\n\n"
        "[bold magenta]Commands:[/bold magenta]\n"
        "  [green]add-api[/green]            Add or update an API key for an AI provider.\n"
        "  [green]remove-api[/green]         Remove a stored API key.\n"
        "  [green]list-api[/green]           List configured AI providers.\n"
        "  [green]generate[/green]           Generate a Git commit message from repository changes.\n"
    )
    console.print(help_text)


def print_command_help(command: str) -> None:
    if command == "add-api":
        console.print(
            "\n[bold cyan]Usage:[/bold cyan] [bold green]Commit.AI add-api[/bold green] [cyan]<provider>[/cyan]\n\n"
            "[bold white]Add or update an API key for an AI provider.[/bold white]\n\n"
            "[bold magenta]Arguments:[/bold magenta]\n"
            "  [green]<provider>[/green]       AI provider to configure.\n"
        )
    elif command == "remove-api":
        console.print(
            "\n[bold cyan]Usage:[/bold cyan] [bold green]Commit.AI remove-api[/bold green] [cyan]<provider>[/cyan]\n\n"
            "[bold white]Remove a stored API key.[/bold white]\n\n"
            "[bold magenta]Arguments:[/bold magenta]\n"
            "  [green]<provider>[/green]       AI provider whose API key should be removed.\n"
        )
    elif command == "list-api":
        console.print(
            "\n[bold cyan]Usage:[/bold cyan] [bold green]Commit.AI list-api[/bold green]\n\n"
            "[bold white]List configured AI providers.[/bold white]\n"
        )
    elif command == "generate":
        console.print(
            "\n[bold cyan]Usage:[/bold cyan] [bold green]Commit.AI generate[/bold green] [cyan]<provider> \\[path][/cyan]\n\n"
            "[bold white]Generate a Git commit message from repository changes.[/bold white]\n\n"
            "[bold magenta]Arguments:[/bold magenta]\n"
            "  [green]<provider>[/green]       AI provider to use for commit message generation.\n"
            "  [green]\\[path][/green]           Path to the Git repository. [dim][default: .][/dim]\n"
        )


def validate_provider(provider_str: str) -> None:
    if provider_str in core.ProviderOptionsList:
        return

    valid_options = ", ".join(core.ProviderOptionsList)
    raise ValueError(f"Invalid provider '{provider_str}'. Choose from: {valid_options}")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print_help()
        sys.exit(0)

    if args[0] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    if args[0] in ("-v", "--version"):
        rich.print(f"[dim]Commit.AI[/dim] [cyan]{VERSION}[/cyan]")
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
        core.AddApi(provider)  # pyright: ignore[reportArgumentType]

    elif command == "remove-api":
        if len(args) > 1 and args[1] in ("-h", "--help"):
            print_command_help(command)
            sys.exit(0)
        if len(args) < 2:
            raise ValueError("Missing required argument: <provider>")
        provider = args[1]
        validate_provider(provider)
        core.RemoveApi(provider)  # pyright: ignore[reportArgumentType]

    elif command == "list-api":
        if len(args) > 1 and args[1] in ("-h", "--help"):
            print_command_help(command)
            sys.exit(0)
        core.ListApi()

    elif command == "generate":
        if len(args) > 1 and args[1] in ("-h", "--help"):
            print_command_help(command)
            sys.exit(0)
        if len(args) < 2:
            raise ValueError("Missing required argument: <provider>")

        provider = args[1]
        validate_provider(provider)

        path_str = args[2] if len(args) > 2 else "."
        path = Path(path_str).resolve()

        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path_str}")
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path_str}")
        if not os.access(path, os.R_OK):
            raise PermissionError(f"Path is not readable: {path_str}")

        core.Generate(path, provider)  # pyright: ignore[reportArgumentType]

    else:
        raise ValueError(
            f"Unknown command: '{command}'. Use --help to list available commands."
        )


if __name__ == "__main__":
    import os

    try:
        main()
    except Exception as e:  # noqa: BLE001
        console.print(f"[bold red]Error:[/bold red] [yellow]{e}[/yellow]")
        sys.exit(1)
