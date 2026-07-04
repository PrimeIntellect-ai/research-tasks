# test_final_state.py

import os
import sqlite3
import pytest
import re

def test_report_output_file():
    """Test that the report output file exists and has the correct content."""
    output_path = "/home/user/report_output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Charlie|500.00",
        "David|450.00",
        "Alice|350.50"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Expected output {expected_lines}, but got {actual_lines}"

def test_executable_exists():
    """Test that the compiled executable exists."""
    exe_path = "/home/user/report"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_cpp_source_code():
    """Test that report.cpp contains JOIN and sqlite3_bind_*."""
    cpp_path = "/home/user/report.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "JOIN" in content.upper(), "The source code does not contain a JOIN query."
    assert "sqlite3_bind_" in content, "The source code does not contain parameterized queries (sqlite3_bind_*)."
    assert "GROUP BY" in content.upper(), "The source code does not contain a GROUP BY clause."

def test_database_index():
    """Test that at least one index was created in the database."""
    db_path = "/home/user/retail.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()

    conn.close()

    assert len(indexes) > 0, "No custom index was created in the database."