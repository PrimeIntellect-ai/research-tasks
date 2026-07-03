# test_final_state.py

import os
import sqlite3
import pytest

def test_artifacts_db_schema_migrated():
    db_path = "/home/user/artifacts.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(packages);")
    columns = {row[1] for row in cursor.fetchall()}

    assert "checksum" in columns, "Column 'checksum' is missing from the packages table."
    assert "dependencies" in columns, "Column 'dependencies' is missing from the packages table."

    conn.close()

def test_artifacts_db_active_packages():
    db_path = "/home/user/artifacts.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query active packages
    cursor.execute("SELECT name, version FROM packages WHERE active=1 ORDER BY name;")
    active_rows = cursor.fetchall()

    expected_active = {
        ("BaseLib", "1.1"),
        ("DataParser", "1.5"),
        ("DataPipeline", "2.0"),
        ("MathLib", "3.0")
    }
    assert set(active_rows) == expected_active, f"Active packages are incorrect. Expected {expected_active}, got {set(active_rows)}"

    # Query inactive packages
    cursor.execute("SELECT name, version FROM packages WHERE active=0 ORDER BY name;")
    inactive_rows = cursor.fetchall()

    expected_inactive = {
        ("BaseLib", "1.0"),
        ("OldTool", "0.9"),
        ("UnusedLib", "1.0")
    }
    assert set(inactive_rows) == expected_inactive, f"Inactive packages are incorrect. Expected {expected_inactive}, got {set(inactive_rows)}"

    conn.close()

def test_rate_limit_test_log():
    log_path = "/home/user/rate_limit_test.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["200", "200", "200", "429"]
    assert lines == expected_lines, f"Rate limit log contents are incorrect. Expected {expected_lines}, got {lines}"