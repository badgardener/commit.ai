from datetime import datetime
from pathlib import Path

from git import (
    BadName,
    GitCommandNotFound,
    InvalidGitRepositoryError,
    NoSuchPathError,
    Repo,
)


class PromptBuildError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __repr__(self) -> str:
        return super().__repr__()

    def __str__(self) -> str:
        return super().__str__()


def GetRawPrompt(path: Path):
    try:
        repo = Repo(path)
    except InvalidGitRepositoryError:
        raise PromptBuildError("Given path is not a valid git repository.")
    except GitCommandNotFound:
        raise PromptBuildError("Git command not found in your path.")
    except NoSuchPathError:
        raise PromptBuildError("Given path is not a folder, or doesn't exists.")

    untracked_files: list[Path] = [
        Path(repo.working_dir) / file for file in repo.untracked_files
    ]
    if not (untracked_files or repo.is_dirty()):
        raise PromptBuildError("Given repository is not changed from last commit.")

    last_commits: list[tuple[str, datetime]] = []
    try:
        last_commits = [
            (str(c.message), c.committed_datetime) for c in repo.iter_commits()
        ]
    except ValueError:
        pass

    diffs: list[tuple[str, str]] = []

    try:
        for d in repo.index.diff("HEAD", create_patch=True):
            if d.a_path:
                diff_text = (
                    d.diff.decode("utf-8", errors="replace")
                    if isinstance(d.diff, bytes)
                    else str(d.diff)
                )
                diffs.append((d.a_path, diff_text))
    except (BadName, ValueError):
        pass

    for d in repo.index.diff(None, create_patch=True):
        if d.a_path:
            diff_text = (
                d.diff.decode("utf-8", errors="replace")
                if isinstance(d.diff, bytes)
                else str(d.diff)
            )
            diffs.append((d.a_path, diff_text))

    commit_history: str = "== == == COMMIT HISTORY == == ==\n\n"
    for commit in last_commits:
        commit_message: str = (
            f"==> {commit[1]}\n{commit[0]}\n\n == == == == == == == ==\n\n"
        )
        commit_history += commit_message

    diff_message: str = "== == == DIFF == == ==\n\n"
    for diff in diffs:
        msg = f"==> {diff[0]}\n\n{diff[1]} \n\n == == == == == == == ==\n\n"
        diff_message += msg

    new_files: str = "== == == NEW FILES == == ==\n\n"
    for f in untracked_files:
        try:
            content: list[str] = f.read_text(encoding="utf-8", errors="replace").split(
                "\n"
            )
            if len(content) >= 256:
                new_files += f"==> {f.resolve()} [LARGE FILE]\n\n"
            else:
                file_msg: str = f"==> {f.resolve()}\n\n{'\n'.join(content)}\n\n == == == == == == == ==\n\n"
                new_files += file_msg
        except (UnicodeDecodeError, PermissionError):
            new_files += f"==> {f.resolve()} [BINARY/UNREADABLE]\n\n"

    raw_prompt: str = ""

    if last_commits and len(last_commits) < 256:
        raw_prompt += commit_history
    if diffs:
        raw_prompt += diff_message
    if untracked_files:
        raw_prompt += new_files

    return raw_prompt
