"""Tests for CLI interface."""

import pytest
from typer.testing import CliRunner
from unittest.mock import Mock, patch, MagicMock
from ai.cli import app

runner = CliRunner()


def test_cli_no_args():
    """Test CLI with no arguments."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0


def test_cli_help():
    """Test CLI help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "terminal assistant" in result.stdout.lower()


@patch("ai.cli.OllamaClient")
@patch("ai.cli.load_config")
@patch("ai.cli.stream_markdown")
@patch("ai.cli.save_message")
def test_cli_with_prompt(mock_save, mock_stream, mock_config, mock_client):
    """Test CLI with a prompt."""
    mock_config.return_value = Mock(
        model="codellama",
        history_size=20,
        ollama_url="http://localhost:11434"
    )
    
    mock_client_instance = Mock()
    mock_client_instance.is_available.return_value = True
    mock_client_instance.chat.return_value = iter(["Hello", " world"])
    mock_client.return_value = mock_client_instance
    
    mock_stream.return_value = "Hello world"
    
    result = runner.invoke(app, ["test prompt"])
    
    assert result.exit_code == 0
    mock_save.assert_called_once()


@patch("ai.cli.OllamaClient")
@patch("ai.cli.load_config")
def test_cli_ollama_not_available(mock_config, mock_client):
    """Test CLI when Ollama is not available."""
    mock_config.return_value = Mock(
        model="codellama",
        history_size=20,
        ollama_url="http://localhost:11434"
    )
    
    mock_client_instance = Mock()
    mock_client_instance.is_available.return_value = False
    mock_client.return_value = mock_client_instance
    
    result = runner.invoke(app, ["test prompt"])
    
    assert result.exit_code == 1
    assert "Could not connect to Ollama" in result.stdout


@patch("ai.cli.is_git_repo")
def test_commit_not_in_repo(mock_is_git):
    """Test commit command outside git repo."""
    mock_is_git.return_value = False
    
    result = runner.invoke(app, ["commit"])
    
    assert result.exit_code == 1
    assert "Not in a git repository" in result.stdout


@patch("ai.cli.is_git_repo")
@patch("ai.cli.get_git_diff")
def test_commit_no_changes(mock_diff, mock_is_git):
    """Test commit command with no changes."""
    mock_is_git.return_value = True
    mock_diff.return_value = ""
    
    result = runner.invoke(app, ["commit"])
    
    assert result.exit_code == 0
    assert "No changes" in result.stdout
