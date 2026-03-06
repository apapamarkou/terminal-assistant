"""Editor integration for editing commit messages."""

import os
import subprocess
import tempfile
from pathlib import Path


def get_editor() -> str:
    """Get the user's preferred editor."""
    return os.environ.get("EDITOR", "nano")


def edit_text(initial_text: str) -> str:
    """Open text in editor and return edited content."""
    editor = get_editor()
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(initial_text)
        f.flush()
        temp_path = f.name
    
    try:
        subprocess.run([editor, temp_path], check=True)
        
        with open(temp_path, "r") as f:
            edited_text = f.read()
        
        return edited_text.strip()
    finally:
        Path(temp_path).unlink(missing_ok=True)
