from pathlib import Path

import rich
from typer import Argument, Option, Typer

import core

VERSION = "26.0.0"

app: Typer = Typer(
    name="Commit.AI",
    help="Generate Git commit messages using AI.",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def version_callback(v: bool) -> None:
    if v:
        rich.print(f"[dim]Commit.AI[/dim] [cyan]{VERSION}[/cyan]")
        raise SystemExit(0)


@app.callback()
def main(
    version: bool = Option(
        False,
        "--version",
        "-v",
        help="Show the Commit.AI version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None: ...


@app.command(
    name="add-api",
    help="Add or update an API key for an AI provider.",
)
def add_api(
    provider: core.ProviderOptions = Argument(  # noqa: B008
        help="AI provider to configure.",
    ),
) -> None:
    core.AddApi(provider)


@app.command(
    name="remove-api",
    help="Remove a stored API key.",
)
def remove_api(
    provider: core.ProviderOptions = Argument(  # noqa: B008
        help="AI provider whose API key should be removed.",
    ),
) -> None:
    core.RemoveApi(provider)


@app.command(
    name="list-api",
    help="List configured AI providers.",
)
def list_api() -> None:
    core.ListApi()


@app.command(
    name="generate",
    help="Generate a Git commit message from repository changes.",
)
def generate(
    path: Path = Argument(  # noqa: B008
        Path("."),
        help="Path to the Git repository.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    provider: core.ProviderOptions = Argument(  # noqa: B008
        help="AI provider to use for commit message generation.",
    ),
) -> None:
    core.Generate(path, provider)


if __name__ == "__main__":
    app()
