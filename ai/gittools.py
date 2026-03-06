"""Git integration tools."""

import subprocess
from pathlib import Path
from typing import Optional


def is_git_repo() -> bool:
    """Check if current directory is in a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True,
            text=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_git_diff() -> Optional[str]:
    """Get the current git diff."""
    if not is_git_repo():
        return None
    
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True,
            check=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def git_commit(message: str) -> tuple[bool, str]:
    """Commit changes with the given message."""
    try:
        result = subprocess.run(
            ["git", "commit", "-am", message],
            check=True,
            capture_output=True,
            text=True
        )
        return True, ""
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() or e.stdout.strip()
        return False, error_msg
