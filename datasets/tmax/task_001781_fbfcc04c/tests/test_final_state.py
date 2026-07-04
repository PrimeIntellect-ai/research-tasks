# test_final_state.py
import os
import sqlite3
import pytest

def test_analysis_db_exists():
    """Test that the analysis.db SQLite database was created."""
    db_path = "/home/user/analysis.db"
    assert os.path.exists(db_path), f"The database file {db_path} is missing."
    assert os.path.isfile(db_path), f"The path {db_path} is not a file."

    # Check if it's a valid SQLite database by connecting
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
        table = cursor.fetchone()
        assert table is not None, "The 'transactions' table is missing from analysis.db."
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to connect to analysis.db or query it: {e}")

def test_indexes_sql_exists_and_valid():
    """Test that indexes.sql exists and contains at least one CREATE INDEX statement."""
    sql_path = "/home/user/indexes.sql"
    assert os.path.exists(sql_path), f"The file {sql_path} is missing."
    assert os.path.isfile(sql_path), f"The path {sql_path} is not a file."

    with open(sql_path, "r") as f:
        content = f.read().upper()

    assert "CREATE " in content and " INDEX " in content, "The file indexes.sql does not contain a CREATE INDEX statement."

def test_peak_concurrency_csv():
    """Test that peak_concurrency.csv contains the correct output."""
    csv_path = "/home/user/peak_concurrency.csv"
    assert os.path.exists(csv_path), f"The file {csv_path} is missing."
    assert os.path.isfile(csv_path), f"The path {csv_path} is not a file."

    expected_lines = [
        "100,2",
        "101,3",
        "102,2"
    ]

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"The contents of {csv_path} do not match the expected output. Expected {expected_lines}, got {lines}."