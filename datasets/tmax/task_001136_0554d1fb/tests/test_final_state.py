# test_final_state.py

import os
import stat
import subprocess
import sqlite3
import pytest

SCRIPT_PATH = "/home/user/get_network.sh"
DB_PATH = "/home/user/company.db"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    st = os.stat(SCRIPT_PATH)
    assert st.st_mode & stat.S_IXUSR, f"Script at {SCRIPT_PATH} is not executable"

def test_indexes_created():
    # Run the script once to ensure indexes are created
    subprocess.run([SCRIPT_PATH, "5", "2", "0"], capture_output=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check for indexes on manager table
    cursor.execute("PRAGMA index_list('manager');")
    indexes = cursor.fetchall()

    # We need to ensure there are indexes covering emp_id and manager_id
    # PRAGMA index_info(index_name) gives columns
    indexed_columns = set()
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        cols = cursor.fetchall()
        if cols:
            # Add the first column of the index
            indexed_columns.add(cols[0][2])

    conn.close()

    assert 'emp_id' in indexed_columns, "Index on manager(emp_id) was not created."
    assert 'manager_id' in indexed_columns, "Index on manager(manager_id) was not created."

def test_script_output_1():
    result = subprocess.run([SCRIPT_PATH, "5", "2", "0"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    expected_output = """Chain: Alice CEO (Executive) -> Charlie VP (Engineering) -> Eve Dir (Engineering)
Subordinates:
7 | Grace Mgr | Engineering
9 | Ivan IC | Engineering
"""
    assert result.stdout.strip() == expected_output.strip(), f"Output mismatch for '5 2 0'. Got:\n{result.stdout}"

def test_script_output_2():
    result = subprocess.run([SCRIPT_PATH, "5", "2", "1"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    expected_output = """Chain: Alice CEO (Executive) -> Charlie VP (Engineering) -> Eve Dir (Engineering)
Subordinates:
9 | Ivan IC | Engineering
10 | Judy IC | Engineering
"""
    assert result.stdout.strip() == expected_output.strip(), f"Output mismatch for '5 2 1'. Got:\n{result.stdout}"

def test_script_output_3():
    result = subprocess.run([SCRIPT_PATH, "3", "10", "0"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    expected_output = """Chain: Alice CEO (Executive) -> Charlie VP (Engineering)
Subordinates:
5 | Eve Dir | Engineering
7 | Grace Mgr | Engineering
9 | Ivan IC | Engineering
10 | Judy IC | Engineering
"""
    assert result.stdout.strip() == expected_output.strip(), f"Output mismatch for '3 10 0'. Got:\n{result.stdout}"