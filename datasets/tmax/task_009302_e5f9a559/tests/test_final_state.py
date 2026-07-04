# test_final_state.py

import os
import sqlite3
import pytest

def test_fixed_query_results():
    fixed_query_path = "/home/user/fixed_query.sql"
    db_path = "/home/user/compliance.db"

    assert os.path.exists(fixed_query_path), f"File {fixed_query_path} does not exist."

    with open(fixed_query_path, 'r') as f:
        query = f.read().strip()

    assert query, f"{fixed_query_path} is empty."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Executing fixed_query.sql failed with error: {e}")
    finally:
        conn.close()

    assert len(results) == 2, f"Expected exactly 2 rows, but got {len(results)} rows."

    # Check if the results match the expected output
    expected_results = {("Alice", "Audit_Logs"), ("Bob", "Audit_Logs")}
    actual_results = set(results)

    assert actual_results == expected_results, f"Query results did not match expected direct accesses for Compliance users. Got: {actual_results}"

def test_cpp_program_exists():
    cpp_path = "/home/user/path_finder.cpp"
    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} does not exist."

def test_shortest_path_output():
    output_path = "/home/user/shortest_path.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    expected_path = "Mallory,Intern_Group,Staff_Group,Admin_Group,Mainframe"
    assert content == expected_path, f"Shortest path output is incorrect. Expected '{expected_path}', but got '{content}'."