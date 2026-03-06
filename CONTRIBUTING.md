# Contributing to Terminal Assistant

Thank you for your interest in contributing to Terminal Assistant!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd terminal-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify setup**
   ```bash
   python setup_check.py
   ```

## Running Tests

```bash
pytest
```

Run with coverage:
```bash
pytest --cov=ai --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_config.py
```

## Code Style

- Follow PEP 8
- Use type hints for all functions
- Add docstrings to public functions
- Keep functions small and focused
- Maximum line length: 100 characters

## Project Structure

```
ai/
├── cli.py           # CLI interface (Typer)
├── ollama_client.py # Ollama API client
├── config.py        # Configuration management
├── history.py       # SQLite history
├── systeminfo.py    # System information
├── gittools.py      # Git integration
├── editor.py        # Editor integration
└── streaming.py     # Streaming output
```

## Adding New Features

### 1. New CLI Command

Add to `ai/cli.py`:
```python
@app.command()
def mycommand():
    """Description of command."""
    # Implementation
```

### 2. New Configuration Option

1. Add to `Config` dataclass in `ai/config.py`
2. Update default config template
3. Add tests in `tests/test_config.py`

### 3. New History Feature

1. Add function to `ai/history.py`
2. Update database schema if needed
3. Add tests in `tests/test_history.py`

## Testing Guidelines

- Write tests for all new features
- Mock external dependencies (Ollama, git)
- Use pytest fixtures for common setup
- Aim for high test coverage
- Test both success and error cases

Example test:
```python
def test_my_feature(tmp_path, monkeypatch):
    """Test description."""
    # Setup
    monkeypatch.setattr("module.function", mock_function)
    
    # Execute
    result = my_feature()
    
    # Assert
    assert result == expected
```

## Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run tests**
   ```bash
   pytest
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed

Examples:
```
Add support for custom models
Fix history search with special characters
Update documentation for commit command
```

## Documentation

Update documentation when:
- Adding new features
- Changing behavior
- Adding configuration options

Documentation files:
- `README.md` - Overview and quick start
- `docs/architecture.md` - System design
- `docs/usage.md` - Detailed usage guide

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about contributing
- Documentation improvements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
