"""Tests for conversation history."""

import tempfile
from pathlib import Path
import pytest
from ai.history import (
    init_db, save_message, get_last_messages, 
    search_messages, get_db_path
)


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Create a temporary database for testing."""
    monkeypatch.setattr("ai.history.Path.home", lambda: tmp_path)
    init_db()
    return get_db_path()


def test_init_db_creates_table(temp_db):
    """Test database initialization."""
    assert temp_db.exists()


def test_save_message(temp_db):
    """Test saving a message."""
    save_message("What is Python?", "Python is a programming language.")
    messages = get_last_messages(1)
    
    assert len(messages) == 1
    assert messages[0].question == "What is Python?"
    assert messages[0].answer == "Python is a programming language."


def test_get_last_messages(temp_db):
    """Test retrieving last N messages."""
    save_message("Question 1", "Answer 1")
    save_message("Question 2", "Answer 2")
    save_message("Question 3", "Answer 3")
    
    messages = get_last_messages(2)
    
    assert len(messages) == 2
    assert messages[0].question == "Question 2"
    assert messages[1].question == "Question 3"


def test_get_last_messages_order(temp_db):
    """Test messages are returned in chronological order."""
    save_message("First", "Answer 1")
    save_message("Second", "Answer 2")
    
    messages = get_last_messages(2)
    
    assert messages[0].question == "First"
    assert messages[1].question == "Second"


def test_search_messages(temp_db):
    """Test searching messages by keyword."""
    save_message("How to use Python?", "Python is easy to use.")
    save_message("What is JavaScript?", "JavaScript is a web language.")
    save_message("Python vs Java", "Python is simpler.")
    
    results = search_messages("Python")
    
    assert len(results) == 2
    assert any("Python" in m.question for m in results)


def test_search_messages_no_results(temp_db):
    """Test search with no matching results."""
    save_message("Question 1", "Answer 1")
    
    results = search_messages("nonexistent")
    
    assert len(results) == 0
