"""Tests for configuration management."""

import tempfile
from pathlib import Path
import pytest
from ai.config import Config, load_config, create_default_config, get_config_path


def test_config_dataclass():
    """Test Config dataclass with default values."""
    config = Config()
    assert config.model == "codellama"
    assert config.history_size == 20
    assert config.ollama_url == "http://localhost:11434"


def test_config_custom_values():
    """Test Config with custom values."""
    config = Config(model="llama2", history_size=10, ollama_url="http://localhost:8080")
    assert config.model == "llama2"
    assert config.history_size == 10
    assert config.ollama_url == "http://localhost:8080"


def test_create_default_config(tmp_path, monkeypatch):
    """Test creating default configuration file."""
    config_dir = tmp_path / ".config" / "ai"
    config_file = config_dir / "config.toml"
    
    monkeypatch.setattr("ai.config.Path.home", lambda: tmp_path)
    
    create_default_config()
    
    assert config_file.exists()
    content = config_file.read_text()
    assert "codellama" in content
    assert "history_size" in content


def test_load_config_creates_default(tmp_path, monkeypatch):
    """Test that load_config creates default if not exists."""
    monkeypatch.setattr("ai.config.Path.home", lambda: tmp_path)
    
    config = load_config()
    
    assert config.model == "codellama"
    assert config.history_size == 20


def test_load_config_reads_existing(tmp_path, monkeypatch):
    """Test loading existing configuration."""
    config_dir = tmp_path / ".config" / "ai"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.toml"
    
    config_file.write_text("""
model = "llama2"
history_size = 15
ollama_url = "http://localhost:9999"
""")
    
    monkeypatch.setattr("ai.config.Path.home", lambda: tmp_path)
    
    config = load_config()
    
    assert config.model == "llama2"
    assert config.history_size == 15
    assert config.ollama_url == "http://localhost:9999"
