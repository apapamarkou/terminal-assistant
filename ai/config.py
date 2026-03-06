"""Configuration management for terminal assistant."""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class Config:
    """Application configuration."""
    
    model: str = "codellama"
    history_size: int = 20
    ollama_url: str = "http://localhost:11434"


def get_config_path() -> Path:
    """Get the configuration file path."""
    config_dir = Path.home() / ".config" / "ai"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.toml"


def create_default_config() -> None:
    """Create default configuration file."""
    config_path = get_config_path()
    default_config = """# Terminal Assistant Configuration

model = "codellama"
history_size = 20
ollama_url = "http://localhost:11434"
"""
    config_path.write_text(default_config)


def load_config() -> Config:
    """Load configuration from file or create default."""
    config_path = get_config_path()
    
    if not config_path.exists():
        create_default_config()
    
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    
    return Config(
        model=data.get("model", "codellama"),
        history_size=data.get("history_size", 20),
        ollama_url=data.get("ollama_url", "http://localhost:11434"),
    )
