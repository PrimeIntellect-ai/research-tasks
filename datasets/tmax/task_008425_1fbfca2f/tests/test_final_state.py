# test_final_state.py
import os
import sqlite3
import subprocess
import pytest

def test_server_compiled():
    server_path = "/home/user/service/server"
    assert os.path.isfile(server_path), f"Expected executable not found at {server_path}"
    assert os.access(server_path, os.X_OK), f"File at {server_path} is not executable"

def test_database_schema():
    db_path = "/home/user/service/db.sqlite3"
    assert os.path.isfile(db_path), f"Database file not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if 'users' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table = cursor.fetchone()
    assert table is not None, "Table 'users' does not exist in the database."

    # Check columns in 'users' table
    cursor.execute("PRAGMA table_info(users);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = ["id", "username", "balance", "coupon_redeemed"]
    for col in expected_columns:
        assert col in columns, f"Column '{col}' missing from 'users' table"

    conn.close()

def test_report_balance():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file not found at {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    try:
        balance = int(content)
    except ValueError:
        pytest.fail(f"Content of {report_path} is not a valid integer: '{content}'")

    assert balance > 50, f"Expected balance to be strictly greater than 50 (race condition exploited), but got {balance}"

def test_venv_and_requests():
    python_path = "/home/user/venv/bin/python"
    assert os.path.isfile(python_path), f"Virtual environment Python not found at {python_path}"
    assert os.access(python_path, os.X_OK), f"Virtual environment Python is not executable"

    # Check if requests is installed in the venv
    result = subprocess.run(
        [python_path, "-c", "import requests"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to import 'requests' in the virtual environment. Error: {result.stderr}"