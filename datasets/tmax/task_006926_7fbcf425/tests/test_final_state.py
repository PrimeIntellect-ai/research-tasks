# test_final_state.py

import os
import sqlite3
import pytest

C_FILE_PATH = "/home/user/process_graph.c"
OUTPUT_FILE_PATH = "/home/user/max_degree.txt"
DB_PATH = "/home/user/graph.db"

def test_c_file_exists():
    assert os.path.exists(C_FILE_PATH), f"C program file {C_FILE_PATH} does not exist."
    assert os.path.isfile(C_FILE_PATH), f"{C_FILE_PATH} is not a file."

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE_PATH), f"Output file {OUTPUT_FILE_PATH} does not exist."
    assert os.path.isfile(OUTPUT_FILE_PATH), f"{OUTPUT_FILE_PATH} is not a file."

def test_output_content():
    # We dynamically compute the expected max from the DB, just in case
    expected_node = None
    expected_weight = -1

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Compute the actual max weighted out-degree
        cursor.execute("SELECT src, SUM(weight) as total_weight FROM edges GROUP BY src ORDER BY total_weight DESC LIMIT 1;")
        row = cursor.fetchone()
        if row:
            expected_node = row[0]
            expected_weight = row[1]
    except sqlite3.Error as e:
        pytest.fail(f"SQLite error occurred while verifying truth: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

    assert expected_node is not None, "Could not compute expected max degree from database."

    expected_output = f"Node: {expected_node}, Total Weight: {expected_weight}"

    with open(OUTPUT_FILE_PATH, 'r') as f:
        content = f.read().strip()

    assert expected_output in content, f"Expected output to contain '{expected_output}', but got '{content}'."