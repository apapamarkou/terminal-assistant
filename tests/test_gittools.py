"""Tests for git integration."""

import subprocess
from pathlib import Path
import pytest
from ai.gittools import is_git_repo, get_git_diff, git_commit


def test_is_git_repo_false(tmp_path, monkeypatch):
    """Test is_git_repo returns False for non-git directory."""
    monkeypatch.chdir(tmp_path)
    assert is_git_repo() is False


def test_is_git_repo_true(tmp_path, monkeypatch):
    """Test is_git_repo returns True for git directory."""
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], capture_output=True)
    
    assert is_git_repo() is True


def test_get_git_diff_no_repo(tmp_path, monkeypatch):
    """Test get_git_diff returns None for non-git directory."""
    monkeypatch.chdir(tmp_path)
    assert get_git_diff() is None


def test_get_git_diff_with_changes(tmp_path, monkeypatch):
    """Test get_git_diff returns diff content."""
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], capture_output=True)
    
    # Create initial commit
    test_file = tmp_path / "test.txt"
    test_file.write_text("initial")
    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], capture_output=True)
    
    # Make changes
    test_file.write_text("modified")
    
    diff = get_git_diff()
    assert diff is not None
    assert "modified" in diff or "test.txt" in diff


def test_git_commit_success(tmp_path, monkeypatch):
    """Test successful git commit."""
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], capture_output=True)
    
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    subprocess.run(["git", "add", "."], capture_output=True)
    
    success, error = git_commit("Test commit")
    assert success is True
    assert error == ""


def test_git_commit_no_changes(tmp_path, monkeypatch):
    """Test git commit with no changes."""
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], capture_output=True)
    
    success, error = git_commit("Empty commit")
    assert success is False
    assert error != ""
