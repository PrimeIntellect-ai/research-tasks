# test_final_state.py

import os
import sqlite3
import pytest

def test_indexes_sql_exists_and_valid():
    """Verify that the SQL script for indexes exists and contains appropriate CREATE INDEX statements."""
    path = "/home/user/indexes.sql"
    assert os.path.exists(path), f"Index creation script {path} does not exist."

    with open(path, "r") as f:
        content = f.read().lower()

    assert "create " in content and "index " in content, f"No CREATE INDEX statement found in {path}."
    assert "server_id" in content or "parent_id" in content, f"Index does not target 'server_id' or 'parent_id' in {path}."

def test_c_program_exists():
    """Verify that the C source file was created."""
    path = "/home/user/analyze_restore.c"
    assert os.path.exists(path), f"C source file {path} does not exist."

def test_executable_exists():
    """Verify that the C program was compiled to the expected executable."""
    path = "/home/user/analyze_restore"
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_restore_report_content():
    """Verify that the restore report contains the correct dynamically computed chain length and size."""
    report_path = "/home/user/restore_report.txt"
    db_path = "/home/user/backups.db"

    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    # Compute the expected values directly from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
        WITH RECURSIVE
          latest_backup AS (
            SELECT id, parent_id, size_bytes
            FROM backups
            WHERE server_id = (SELECT id FROM servers WHERE hostname = 'db-master-42')
            ORDER BY created_at DESC
            LIMIT 1
          ),
          chain AS (
            SELECT id, parent_id, size_bytes
            FROM latest_backup
            UNION ALL
            SELECT b.id, b.parent_id, b.size_bytes
            FROM backups b
            JOIN chain c ON b.id = c.parent_id
          )
        SELECT COUNT(*), SUM(size_bytes) FROM chain;
    """

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Failed to compute backup chain from the database."
    expected_length, expected_total_size = result

    expected_content = f"Server: db-master-42 | Chain Length: {expected_length} | Total Size: {expected_total_size} bytes"

    with open(report_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Report content mismatch.\n"
        f"Expected: '{expected_content}'\n"
        f"Actual:   '{actual_content}'"
    )