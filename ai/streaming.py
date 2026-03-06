"""Streaming output with markdown rendering."""

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown


def stream_markdown(chunks: iter) -> str:
    """Stream markdown content to terminal and return full text."""
    console = Console()
    full_text = ""
    
    with Live("", console=console, refresh_per_second=10) as live:
        for chunk in chunks:
            full_text += chunk
            md = Markdown(full_text)
            live.update(md)
    
    return full_text
