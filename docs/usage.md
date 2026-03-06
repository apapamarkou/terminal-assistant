# Usage Guide

## Installation

### Prerequisites

1. Install Python 3.11 or higher
2. Install Ollama from https://ollama.ai/

### Install Terminal Assistant

```bash
cd terminal-assistant
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Getting Started

### 1. Start Ollama

```bash
ollama serve
```

### 2. Pull a Model

```bash
ollama pull codellama
```

### 3. Ask Your First Question

```bash
ai "how do I list files in Python?"
```

## Basic Usage

### Ask Questions

```bash
ai "explain list comprehensions in Python"
```

The assistant will:
- Include your system information for context
- Reference previous conversation history
- Stream the response with markdown formatting

### Multi-word Prompts

Use quotes for prompts with spaces:
```bash
ai "what is the difference between lists and tuples?"
```

## Git Integration

### Generate Commit Messages

```bash
# Make some changes
echo "new feature" >> file.txt

# Stage changes
git add .

# Generate commit message
ai commit
```

The tool will:
1. Analyze your git diff
2. Generate a commit message
3. Open it in your editor
4. Ask for confirmation
5. Commit if you approve

### Editor Configuration

Set your preferred editor:
```bash
export EDITOR=vim
```

Supported editors: vim, emacs, nano, code, etc.

## Configuration

### Config File Location

`~/.config/ai/config.toml`

### Default Configuration

```toml
model = "codellama"
history_size = 20
ollama_url = "http://localhost:11434"
```

### Change Model

Edit config file:
```toml
model = "llama2"
```

Or use a different model:
```toml
model = "mistral"
```

### Adjust History Size

```toml
history_size = 50  # Keep last 50 messages
```

### Custom Ollama URL

If running Ollama on a different port:
```toml
ollama_url = "http://localhost:8080"
```

## Examples

### Python Help

```bash
ai "how do I read a JSON file in Python?"
```

### Shell Commands

```bash
ai "find all .py files modified in the last 7 days"
```

### Git Questions

```bash
ai "how do I undo the last commit?"
```

### Debugging

```bash
ai "why am I getting a KeyError in Python?"
```

### Code Review

```bash
ai "review this function: def add(a, b): return a + b"
```

## Conversation History

The assistant remembers your conversation within the session. History is stored in:

`~/.local/share/ai/history.db`

The last N messages (default: 20) are included in each prompt for context.

## Tips

### 1. Be Specific

Instead of:
```bash
ai "python error"
```

Try:
```bash
ai "how to fix ImportError: No module named 'requests'"
```

### 2. Include Context

```bash
ai "I'm using Python 3.11 on Ubuntu. How do I install pip?"
```

### 3. Use for Quick Reference

```bash
ai "git command to show last 5 commits"
```

### 4. Commit Messages

Let AI help with commit messages:
```bash
ai commit
```

Then edit if needed before confirming.

## Troubleshooting

### Ollama Not Running

```
Error: Could not connect to Ollama
```

**Solution**: Start Ollama
```bash
ollama serve
```

### Model Not Found

```
Error: Model 'codellama' not found
```

**Solution**: Pull the model
```bash
ollama pull codellama
```

### Not in Git Repository

```
Error: Not in a git repository
```

**Solution**: Run `ai commit` from within a git repository

### Slow Responses

- Check Ollama is running properly
- Try a smaller model (e.g., `llama2` instead of `codellama`)
- Check system resources

### Database Errors

If you encounter database issues, you can reset history:
```bash
rm ~/.local/share/ai/history.db
```

## Advanced Usage

### Custom System Prompts

Edit the `build_prompt()` function in `ai/cli.py` to customize how prompts are constructed.

### Multiple Models

Switch models by editing `~/.config/ai/config.toml`:
```toml
model = "mistral"
```

### Scripting

Use in scripts:
```bash
#!/bin/bash
ANSWER=$(ai "best practice for error handling in bash")
echo "$ANSWER"
```

## Best Practices

1. **Keep prompts clear and specific**
2. **Use commit command for better commit messages**
3. **Review AI suggestions before executing commands**
4. **Adjust history_size based on your needs**
5. **Use appropriate models for your tasks**

## Getting Help

```bash
ai --help
```

For commit command help:
```bash
ai commit --help
```
