"""Conversation history management using SQLite."""

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List


@dataclass
class Message:
    """A conversation message."""
    
    id: int
    timestamp: str
    question: str
    answer: str


def get_db_path() -> Path:
    """Get the database file path."""
    data_dir = Path.home() / ".local" / "share" / "ai"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "history.db"


def init_db() -> None:
    """Initialize the database schema."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def save_message(question: str, answer: str) -> None:
    """Save a message to the database."""
    init_db()
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO messages (timestamp, question, answer) VALUES (?, ?, ?)",
        (timestamp, question, answer)
    )
    
    conn.commit()
    conn.close()


def get_last_messages(n: int) -> List[Message]:
    """Get the last N messages from history."""
    init_db()
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, timestamp, question, answer FROM messages ORDER BY id DESC LIMIT ?",
        (n,)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    messages = [Message(id=r[0], timestamp=r[1], question=r[2], answer=r[3]) for r in reversed(rows)]
    return messages


def search_messages(keyword: str) -> List[Message]:
    """Search messages by keyword."""
    init_db()
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        """SELECT id, timestamp, question, answer FROM messages 
           WHERE question LIKE ? OR answer LIKE ? 
           ORDER BY id DESC""",
        (f"%{keyword}%", f"%{keyword}%")
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    messages = [Message(id=r[0], timestamp=r[1], question=r[2], answer=r[3]) for r in rows]
    return messages
