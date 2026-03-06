"""CLI interface for terminal assistant."""

import sys
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel

from ai.config import load_config
from ai.history import save_message, get_last_messages
from ai.systeminfo import get_system_info
from ai.ollama_client import OllamaClient
from ai.streaming import stream_markdown
from ai.gittools import is_git_repo, get_git_diff, git_commit
from ai.editor import edit_text

app = typer.Typer(help="AI-powered terminal assistant using Ollama", no_args_is_help=False)
console = Console()


def build_prompt(user_prompt: str, config) -> list:
    """Build the full prompt with system info and history."""
    system_info = get_system_info()
    history = get_last_messages(config.history_size)
    
    messages = []
    
    # System message
    system_content = f"You are a helpful terminal assistant. System information:\n{system_info}"
    messages.append({"role": "system", "content": system_content})
    
    # Add conversation history
    for msg in history:
        messages.append({"role": "user", "content": msg.question})
        messages.append({"role": "assistant", "content": msg.answer})
    
    # Add current prompt
    messages.append({"role": "user", "content": user_prompt})
    
    return messages


@app.command()
def commit():
    """Generate a git commit message from current changes."""
    if not is_git_repo():
        console.print("[red]Error: Not in a git repository[/red]")
        raise typer.Exit(code=1)
    
    diff = get_git_diff()
    if not diff or not diff.strip():
        console.print("[yellow]No changes to commit[/yellow]")
        return
    
    config = load_config()
    client = OllamaClient(config.ollama_url)
    
    if not client.is_available():
        console.print("[red]Error: Could not connect to Ollama. Is it running?[/red]")
        raise typer.Exit(1)
    
    console.print("[cyan]Generating commit message...[/cyan]")
    
    prompt = f"Generate a concise git commit message for these changes. Return only the commit message, no explanation:\n\n{diff}"
    messages = [{"role": "user", "content": prompt}]
    
    try:
        chunks = client.chat(config.model, messages)
        commit_message = "".join(chunks).strip()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    
    # Open in editor
    edited_message = edit_text(commit_message)
    
    if not edited_message:
        console.print("[yellow]Commit message is empty. Aborting.[/yellow]")
        raise typer.Exit(0)
    
    # Show edited message
    console.print(Panel(edited_message, title="Commit Message"))
    
    # Confirm
    confirm = typer.confirm("Commit with this message?")
    if not confirm:
        console.print("[yellow]Commit cancelled[/yellow]")
        return
    
    # Commit
    if git_commit(edited_message):
        console.print("[green]✓ Committed successfully[/green]")
    else:
        console.print("[red]Error: Commit failed[/red]")
        raise typer.Exit(1)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    prompt: Optional[str] = typer.Argument(None, help="Your question or prompt"),
):
    """Ask the AI assistant a question."""
    # If a subcommand was invoked, don't process as a prompt
    if ctx.invoked_subcommand is not None:
        return
    
    # Check if the prompt is actually a command name
    if prompt == "commit":
        ctx.invoke(commit)
        return
    
    if not prompt:
        console.print("[yellow]Usage: ai [PROMPT] or ai commit[/yellow]")
        return
    
    config = load_config()
    client = OllamaClient(config.ollama_url)
    
    if not client.is_available():
        console.print("[red]Error: Could not connect to Ollama. Is it running?[/red]")
        console.print("[yellow]Start Ollama with: ollama serve[/yellow]")
        raise typer.Exit(1)
    
    messages = build_prompt(prompt, config)
    
    try:
        chunks = client.chat(config.model, messages)
        answer = stream_markdown(chunks)
        
        # Save to history
        save_message(prompt, answer)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
