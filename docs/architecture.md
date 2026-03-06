# Architecture

## Overview

Terminal Assistant is a modular CLI application that integrates with local Ollama models to provide AI assistance directly in the terminal.

## Components

### 1. CLI Interface (`cli.py`)

The main entry point using Typer framework. Handles:
- Command parsing and routing
- User interaction
- Error handling and display

### 2. Configuration (`config.py`)

Manages application configuration:
- TOML-based configuration file
- Default values
- Config file creation and loading
- Location: `~/.config/ai/config.toml`

### 3. Ollama Client (`ollama_client.py`)

HTTP client for Ollama API:
- Streaming chat requests
- Connection management
- Error handling
- Supports `/api/chat` endpoint

### 4. History Management (`history.py`)

SQLite-based conversation history:
- Message storage and retrieval
- Search functionality
- Database schema management
- Location: `~/.local/share/ai/history.db`

### 5. System Information (`systeminfo.py`)

Collects system context:
- OS and kernel version
- CPU information
- RAM capacity
- Uses `platform` and `psutil`

### 6. Git Integration (`gittools.py`)

Git repository operations:
- Repository detection
- Diff extraction
- Commit execution
- Uses subprocess to call git commands

### 7. Editor Integration (`editor.py`)

Text editing functionality:
- Respects `$EDITOR` environment variable
- Temporary file management
- Fallback to nano

### 8. Streaming Output (`streaming.py`)

Real-time response rendering:
- Markdown formatting
- Live terminal updates
- Uses Rich library

## Data Flow

### Standard Query Flow

```
User Input → CLI → Config → History → System Info → Prompt Builder
                                                          ↓
                                                    Ollama Client
                                                          ↓
                                                   Stream Response
                                                          ↓
                                              Markdown Renderer → Terminal
                                                          ↓
                                                   Save to History
```

### Commit Flow

```
User: ai commit → Git Detection → Get Diff → Build Prompt
                                                   ↓
                                             Ollama Client
                                                   ↓
                                          Generate Message
                                                   ↓
                                            Open in Editor
                                                   ↓
                                          User Confirmation
                                                   ↓
                                            Git Commit
```

## Design Principles

### Modularity

Each component has a single responsibility and can be tested independently.

### Error Handling

Clear error messages guide users to resolve issues (e.g., Ollama not running, not in git repo).

### User Experience

- Streaming responses for immediate feedback
- Markdown rendering for readable output
- Conversation history for context
- System information for relevant answers

### Configuration

Sensible defaults with easy customization via TOML config file.

## Dependencies

- **Typer**: CLI framework
- **Rich**: Terminal formatting and markdown
- **Requests**: HTTP client for Ollama
- **psutil**: System information
- **SQLite**: Built-in database (no external dependency)

## Testing Strategy

- Unit tests for each module
- Mocking external dependencies (git, Ollama API)
- Temporary directories for file operations
- pytest fixtures for common setup

## Extension Points

The architecture supports easy extension:

1. **New Commands**: Add to `cli.py` with `@app.command()`
2. **Additional Models**: Configure in `config.toml`
3. **Custom Prompts**: Modify `build_prompt()` in `cli.py`
4. **History Features**: Extend `history.py` with new queries
