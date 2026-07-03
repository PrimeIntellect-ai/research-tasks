# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

SCRIPT_PATH = "/home/user/analyze_graph.sh"
DB_PATH = "/home/user/graph.db"

def test_script_exists_and_executable():
    """Test that the analyze_graph.sh script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_page_1():
    """Test the script output for page 1, size 3."""
    result = subprocess.run([SCRIPT_PATH, "1", "3"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    expected_output = "1,4,3\n2,4,3\n1,2,2"
    actual_output = result.stdout.strip()
    assert actual_output == expected_output, f"Expected output:\n{expected_output}\nGot:\n{actual_output}"

def test_script_execution_page_2():
    """Test the script output for page 2, size 3."""
    result = subprocess.run([SCRIPT_PATH, "2", "3"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    expected_output = "1,3,2\n1,5,2\n3,4,2"
    actual_output = result.stdout.strip()
    assert actual_output == expected_output, f"Expected output:\n{expected_output}\nGot:\n{actual_output}"

def test_database_exists():
    """Test that the graph.db database was created."""
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} was not created."
    assert os.path.isfile(DB_PATH), f"{DB_PATH} is not a file."

def test_database_schema_and_indexes():
    """Test that the transactions table has indexes and user_graph is materialized."""
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if transactions table exists
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='transactions';")
    assert cursor.fetchone()[0] == 1, "Table 'transactions' does not exist in the database."

    # Check if indexes exist on transactions table
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='transactions';")
    index_count = cursor.fetchone()[0]
    assert index_count >= 1, "No indexes were created on the 'transactions' table."

    # Check if user_graph table exists
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='user_graph';")
    assert cursor.fetchone()[0] == 1, "Table 'user_graph' was not materialized."

    conn.close()

def test_user_graph_content():
    """Test that the user_graph table contains the correct materialized data."""
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT user1, user2, weight FROM user_graph ORDER BY weight DESC, user1 ASC, user2 ASC;")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query user_graph: {e}")
    finally:
        conn.close()

    expected_rows = [
        (1, 4, 3),
        (2, 4, 3),
        (1, 2, 2),
        (1, 3, 2),
        (1, 5, 2),
        (3, 4, 2),
        (4, 5, 2)
    ]

    # Convert types to strings to handle potential type mismatches from CSV import
    rows_str = [(str(r[0]), str(r[1]), int(r[2])) for r in rows]
    expected_rows_str = [(str(r[0]), str(r[1]), int(r[2])) for r in expected_rows]

    assert rows_str == expected_rows_str, f"Materialized user_graph data is incorrect. Expected {expected_rows_str}, got {rows_str}"