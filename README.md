# Terminal Assistant

AI-powered terminal assistant using local Ollama models. Get instant help, generate commit messages, and interact with AI directly from your command line.

## Features

- 🤖 Chat with local Ollama models (default: codellama)
- 💬 Conversation history stored in SQLite
- 🎨 Beautiful markdown rendering with syntax highlighting
- 📝 AI-powered git commit message generation
- 🖥️ Automatic system context inclusion
- ⚡ Streaming responses for real-time feedback

## Requirements

- Python 3.11+
- [Ollama](https://ollama.ai/) running locally

## Installation

### Recommended (pipx)

Install `pipx` if you don't have it:

```bash
pip install pipx
pipx ensurepath
```
Then install `terminal-assistant`:

```bash
pipx install git+https://github.com/apapamarkou/terminal-assistant
```

## Quick Start

```bash
# Start Ollama (if not already running)
ollama serve

# Pull the default model
ollama pull codellama

# Ask a question
ai "how do I parse JSON in Python?"

# Generate a git commit message
ai commit
```

## Usage

### Basic Chat

```bash
ai "your question here"
```

The assistant will:
- Include system information (OS, CPU, RAM)
- Reference conversation history
- Stream the response with markdown formatting

### Git Commit Messages

```bash
# Stage your changes
git add .

# Generate commit message
ai commit
```

The tool will:
1. Analyze your git diff
2. Generate a concise commit message
3. Open it in your editor for review
4. Prompt for confirmation before committing

## Configuration

Configuration file: `~/.config/ai/config.toml`

Default configuration:
```toml
model = "codellama"
history_size = 20
ollama_url = "http://localhost:11434"
```

The config file is created automatically on first run.

## Data Storage

- **Config**: `~/.config/ai/config.toml`
- **History**: `~/.local/share/ai/history.db`

## Development

### Setup

```bash
# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Project Structure

```
terminal-assistant/
├── ai/                 # Main package
│   ├── cli.py         # CLI interface
│   ├── ollama_client.py  # Ollama API client
│   ├── config.py      # Configuration management
│   ├── history.py     # Conversation history
│   ├── systeminfo.py  # System information
│   ├── gittools.py    # Git integration
│   ├── editor.py      # Editor integration
│   └── streaming.py   # Streaming output
├── tests/             # Test suite
└── docs/              # Documentation
```

## Documentation

- [Architecture](docs/architecture.md) - System design and components
- [Usage Guide](docs/usage.md) - Detailed usage examples

## Troubleshooting

### Ollama not running
```
Error: Could not connect to Ollama
```
Start Ollama: `ollama serve`

### Model not found
```
Error: Model 'codellama' not found
```
Pull the model: `ollama pull codellama`

### Not in a git repository
```
Error: Not in a git repository
```
Run `ai commit` from within a git repository.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
