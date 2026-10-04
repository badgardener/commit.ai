# Commit.AI

Commit.AI is a command-line tool that analyzes your Git repository and generates a concise, conventional-commit message using an AI provider of your choice. It inspects the current diff, recently committed history, and newly added files, then asks an LLM to produce a commit summary that fits the repository’s actual changes.

It is designed for developers who want faster, more consistent commit messages without having to manually draft them each time.

## Features

- Generate commit messages from the current Git working tree
- Support multiple AI providers:
  - OpenAI
  - OpenRouter
  - Groq
  - Google GenAI
  - Anthropic
- Store API keys securely using the OS keyring
- Keep commit history and diff context in the generated prompt
- Enforce conventional commit formatting in the generated output
- Work from any Git repository path

## How it works

The tool builds a prompt from repository state and sends it to an AI model:

1. It checks whether the target path is a valid Git repository.
2. It collects:
   - staged and unstaged diffs
   - untracked files
   - recent commit history
3. It formats the information into a structured prompt.
4. It asks the selected provider for a conventional commit message.
5. It returns a commit summary in this style:

```text
feat: add user dashboard filtering

- add filter controls for customer list
- update query parameters for dashboard state
- improve empty-state messaging when no results match
```

## Supported providers

The current implementation supports these providers:

- `openai`
- `openrouter`
- `groq`
- `genai`
- `anthropic`

Each provider has dedicated request logic and fallback handling for quota or rate-limit issues.

## Requirements

- Python 3.10+
- Git installed and available on your system
- An API key for at least one supported provider

## Installation

Clone the project and install the dependencies:

```bash
git clone <your-repo-url>
cd commit.ai
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

The app stores API keys in the system keyring, so they are kept out of your project files.

To add or update a provider key:

```bash
python -m src.main add-api openai
```

This prompts for the API key and stores it securely for later use.

To list configured providers:

```bash
python -m src.main list-api
```

To remove a stored key:

```bash
python -m src.main remove-api openai
```

## Usage

Generate a commit message for the current repository:

```bash
python -m src.main generate . openai
```

Generate a commit message for a specific repository path:

```bash
python -m src.main generate /path/to/project openrouter
```

Show the app version:

```bash
python -m src.main --version
```

Show the built-in help:

```bash
python -m src.main --help
```

## Command reference

### `add-api`

Adds or updates a stored API key for a provider.

```bash
python -m src.main add-api <provider>
```

Examples:

```bash
python -m src.main add-api openai
python -m src.main add-api anthropic
python -m src.main add-api groq
```

### `remove-api`

Removes the stored key for a provider.

```bash
python -m src.main remove-api <provider>
```

### `list-api`

Lists the providers that currently have a configured API key.

```bash
python -m src.main list-api
```

### `generate`

Generates a commit message from the repo state using the selected provider.

```bash
python -m src.main generate <path> <provider>
```

Arguments:

- `path`: repository directory to inspect
- `provider`: one of `openai`, `openrouter`, `groq`, `genai`, `anthropic`

## Project structure

```text
commit.ai/
├── LICENSE
├── README.md
├── requirements.txt
└── src/
    ├── ai.py
    ├── api_key.py
    ├── core.py
    ├── main.py
    ├── prompt.py
    └── provider/
        ├── __init__.py
        ├── anthropic.py
        ├── error.py
        ├── genai.py
        ├── groq.py
        ├── openai.py
        └── openrouter.py
```

## Notes on implementation

The project uses:

- `typer` for the CLI
- `rich` for terminal output
- `GitPython` to inspect repository state
- `keyring` to store secrets securely
- provider-specific SDKs for AI model access

The prompt builder gathers repository changes and forms instructions that tell the model to respond in conventional commit format. This keeps the output short, structured, and easier to review before committing.

## Example workflow

```bash
cd my-project
python -m venv .venv
source .venv/bin/activate
python -m pip install -r /path/to/commit.ai/requirements.txt
cd /path/to/commit.ai
python -m src.main add-api openai
python -m src.main generate /path/to/my-project openai
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
