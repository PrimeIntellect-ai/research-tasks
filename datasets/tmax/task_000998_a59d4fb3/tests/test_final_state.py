# test_final_state.py
import os
import sqlite3
import pytest

def test_solution_txt():
    solution_path = '/home/user/solution.txt'
    assert os.path.isfile(solution_path), f"Expected solution file {solution_path} does not exist."

    with open(solution_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {solution_path}, found {len(lines)}."

    assert lines[0] == "30", f"Expected total transit time to be '30', got '{lines[0]}'."
    assert lines[1] == "1,3,4,5", f"Expected path to be '1,3,4,5', got '{lines[1]}'."

def test_schema_sql():
    schema_path = '/home/user/schema.sql'
    assert os.path.isfile(schema_path), f"Expected schema file {schema_path} does not exist."

    with open(schema_path, 'r') as f:
        content = f.read().upper()

    index_count = content.count("CREATE INDEX")
    assert index_count >= 2, f"Expected at least 2 CREATE INDEX statements in {schema_path}, found {index_count}."

def test_network_db():
    db_path = '/home/user/network.db'
    assert os.path.isfile(db_path), f"Expected database file {db_path} does not exist."

    # Try connecting to ensure it's a valid SQLite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to connect to SQLite database at {db_path}: {e}")

    assert len(tables) > 0, f"Expected at least one table in the database {db_path}."