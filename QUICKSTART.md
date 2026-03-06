# Quick Start Guide

Get up and running with Terminal Assistant in 5 minutes.

## Prerequisites

- Python 3.11+
- Ollama installed

## Installation

```bash
# 1. Navigate to project directory
cd terminal-assistant

# 2. Install the package
pip install -e .

# 3. Verify installation
python setup_check.py
```

## First Run

```bash
# 1. Start Ollama (in a separate terminal)
ollama serve

# 2. Pull the default model
ollama pull codellama

# 3. Ask your first question
ai "what is Python?"
```

## Basic Commands

### Ask Questions
```bash
ai "how do I read a file in Python?"
```

### Generate Commit Messages
```bash
# Make changes and stage them
git add .

# Generate commit message
ai commit
```

## Configuration

Config file is auto-created at: `~/.config/ai/config.toml`

```toml
model = "codellama"
history_size = 20
ollama_url = "http://localhost:11434"
```

## Troubleshooting

### "Could not connect to Ollama"
Start Ollama: `ollama serve`

### "Model not found"
Pull the model: `ollama pull codellama`

### "Not in a git repository"
Run `ai commit` from inside a git repo

## Next Steps

- Read [Usage Guide](docs/usage.md) for detailed examples
- Check [Architecture](docs/architecture.md) to understand the design
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Examples

```bash
# Python help
ai "explain decorators in Python"

# Shell commands
ai "find all files larger than 100MB"

# Git help
ai "how to rebase my branch"

# Debugging
ai "what causes a segmentation fault"

# Generate commit message
ai commit
```

## Tips

1. Use quotes for multi-word prompts
2. Be specific in your questions
3. The assistant remembers conversation history
4. Review AI-generated commit messages before confirming

Enjoy using Terminal Assistant! 🚀
