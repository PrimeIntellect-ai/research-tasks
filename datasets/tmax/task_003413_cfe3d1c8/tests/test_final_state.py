# test_final_state.py

import os
import sqlite3
from pathlib import Path

def test_db_exists():
    """Test that the SQLite database file exists."""
    db_path = Path("/home/user/report.db")
    assert db_path.exists(), f"Database file {db_path} is missing."
    assert db_path.is_file(), f"Path {db_path} is not a file."

def test_db_schema_and_content():
    """Test the schema and content of the SQLite database."""
    db_path = Path("/home/user/report.db")
    assert db_path.exists(), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='suspicious_ips';")
    assert cursor.fetchone() is not None, "Table 'suspicious_ips' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(suspicious_ips);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}
    assert "ip" in columns, "Column 'ip' is missing from 'suspicious_ips'."
    assert "attempts" in columns, "Column 'attempts' is missing from 'suspicious_ips'."

    # Check data
    cursor.execute("SELECT ip, attempts FROM suspicious_ips ORDER BY attempts DESC, ip ASC;")
    rows = cursor.fetchall()

    expected_data = [
        ("198.51.100.0", 4),
        ("192.0.2.0", 2),
        ("203.0.113.0", 1)
    ]

    assert rows == expected_data, f"Database content is incorrect. Expected {expected_data}, got {rows}."

    # Check sum of attempts
    cursor.execute("SELECT SUM(attempts) FROM suspicious_ips;")
    total_attempts = cursor.fetchone()[0]
    assert total_attempts == 7, f"Expected 7 total attempts, got {total_attempts}."

    conn.close()

def test_top_threats_file():
    """Test that the exported findings file exists and has the correct content."""
    txt_path = Path("/home/user/top_threats.txt")
    assert txt_path.exists(), f"File {txt_path} is missing."
    assert txt_path.is_file(), f"Path {txt_path} is not a file."

    with open(txt_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "198.51.100.0,4",
        "192.0.2.0,2",
        "203.0.113.0,1"
    ]

    assert lines == expected_lines, f"File content of {txt_path} is incorrect. Expected {expected_lines}, got {lines}."