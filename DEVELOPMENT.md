# Development Guide

## Project Overview

Terminal Assistant is a production-quality CLI tool that provides AI assistance in the terminal using local Ollama models.

## Technology Stack

- **Python 3.11+**: Modern Python with native TOML support
- **Typer**: CLI framework with automatic help generation
- **Rich**: Terminal formatting and markdown rendering
- **Requests**: HTTP client for Ollama API
- **SQLite**: Conversation history storage
- **psutil**: System information collection
- **pytest**: Testing framework

## Architecture

### Core Modules

1. **cli.py** - Entry point, command routing, user interaction
2. **ollama_client.py** - HTTP client for Ollama API with streaming
3. **config.py** - TOML configuration management
4. **history.py** - SQLite database operations
5. **systeminfo.py** - System context collection
6. **gittools.py** - Git repository operations
7. **editor.py** - Text editor integration
8. **streaming.py** - Real-time markdown rendering

### Data Flow

```
User Input → CLI Parser → Config Loader → Context Builder
                                              ↓
                                        Ollama Client
                                              ↓
                                      Stream Processor
                                              ↓
                                    Markdown Renderer
                                              ↓
                                      History Storage
```

## Development Workflow

### Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Verify setup
python setup_check.py
```

### Running Locally

```bash
# Run the CLI
ai "test prompt"

# Run specific command
ai commit
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=ai
```

### Code Style

Follow PEP 8 guidelines:
- Use type hints
- Add docstrings
- Keep functions small
- Use descriptive names
- Maximum line length: 100

Example:
```python
def get_system_info() -> str:
    """
    Collect and format system information.
    
    Returns:
        Formatted string with OS, CPU, and RAM info
    """
    # Implementation
```

## Adding Features

### New CLI Command

1. Add command to `ai/cli.py`:
```python
@app.command()
def mycommand(arg: str = typer.Argument(..., help="Description")):
    """Command description."""
    # Implementation
```

2. Add tests to `tests/test_cli.py`
3. Update documentation

### New Configuration Option

1. Add to `Config` dataclass in `ai/config.py`
2. Update default config template
3. Add to `config.example.toml`
4. Add tests
5. Update documentation

### New Database Feature

1. Add function to `ai/history.py`
2. Update schema if needed (with migration)
3. Add tests
4. Document usage

## Testing Strategy

### Unit Tests

Test individual functions in isolation:
```python
def test_get_system_info():
    info = get_system_info()
    assert "OS:" in info
    assert "RAM:" in info
```

### Integration Tests

Test component interactions:
```python
@patch("ai.cli.OllamaClient")
def test_cli_with_prompt(mock_client):
    # Test CLI with mocked Ollama
```

### Mocking

Mock external dependencies:
```python
@patch("ai.gittools.subprocess.run")
def test_git_diff(mock_run):
    mock_run.return_value = Mock(stdout="diff content")
    result = get_git_diff()
    assert result == "diff content"
```

## Debugging

### Enable Verbose Output

```python
# In cli.py, add debug prints
console.print(f"[dim]Debug: {variable}[/dim]")
```

### Test Database

```python
# Inspect database
import sqlite3
conn = sqlite3.connect("~/.local/share/ai/history.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM messages")
print(cursor.fetchall())
```

### Test Ollama Connection

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Test chat endpoint
curl http://localhost:11434/api/chat -d '{
  "model": "codellama",
  "messages": [{"role": "user", "content": "test"}],
  "stream": false
}'
```

## Common Tasks

### Update Dependencies

```bash
pip install --upgrade typer rich requests psutil
```

### Run Linter

```bash
pip install flake8
flake8 ai/ tests/
```

### Format Code

```bash
pip install black
black ai/ tests/
```

### Type Checking

```bash
pip install mypy
mypy ai/
```

## Release Process

1. Update version in `pyproject.toml` and `ai/__init__.py`
2. Update CHANGELOG.md
3. Run all tests: `pytest`
4. Build package: `python -m build`
5. Tag release: `git tag v0.1.0`
6. Push: `git push --tags`

## Troubleshooting

### Import Errors

```bash
# Reinstall in development mode
pip install -e .
```

### Test Failures

```bash
# Run with verbose output
pytest -v -s

# Run specific test
pytest tests/test_config.py::test_load_config -v
```

### Database Issues

```bash
# Reset database
rm ~/.local/share/ai/history.db
```

## Performance Optimization

### Reduce Latency

- Use smaller models (llama2 vs codellama)
- Reduce history_size
- Optimize prompt construction

### Memory Usage

- Limit history_size
- Clear old messages periodically
- Use streaming for large responses

## Security Considerations

- Never log sensitive data
- Sanitize user input
- Validate file paths
- Use subprocess safely
- Handle errors gracefully

## Best Practices

1. **Write tests first** - TDD approach
2. **Keep functions small** - Single responsibility
3. **Use type hints** - Better IDE support
4. **Document public APIs** - Clear docstrings
5. **Handle errors** - Graceful degradation
6. **Mock external calls** - Fast, reliable tests
7. **Use fixtures** - DRY test setup

## Resources

- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [pytest Documentation](https://docs.pytest.org/)

## Getting Help

- Check existing issues
- Read documentation
- Run `python setup_check.py`
- Ask in discussions

Happy coding! 🚀
