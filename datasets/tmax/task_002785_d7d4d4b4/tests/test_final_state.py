# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

def test_find_mutual_sh_output_1():
    script_path = "/home/user/find_mutual.sh"
    assert os.path.exists(script_path), f"Script {script_path} not found."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    try:
        result = subprocess.run(
            [script_path, "U1", "2", "0"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with error: {e.stderr}")

    output = result.stdout.strip().split('\n')
    expected = ["U7,3", "U5,2"]
    assert output == expected, f"Expected output {expected}, but got {output}"

def test_find_mutual_sh_output_2():
    script_path = "/home/user/find_mutual.sh"
    try:
        result = subprocess.run(
            [script_path, "U1", "2", "1"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with error: {e.stderr}")

    output = result.stdout.strip().split('\n')
    expected = ["U5,2", "U6,1"]
    assert output == expected, f"Expected output {expected}, but got {output}"

def test_indexes_created():
    db_path = "/home/user/graph.db"
    assert os.path.exists(db_path), f"Database {db_path} not found."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom indexes found on the 'edges' table. You must create indexes to optimize the query."

def test_query_plan_exists_and_contains_index():
    plan_path = "/home/user/query_plan.txt"
    assert os.path.exists(plan_path), f"File {plan_path} does not exist."
    assert os.path.isfile(plan_path), f"{plan_path} is not a file."

    with open(plan_path, 'r') as f:
        content = f.read().upper()

    assert content.strip() != "", f"File {plan_path} is empty."
    # The query plan should ideally indicate an index scan or covering index
    assert "INDEX" in content or "SEARCH" in content, f"query_plan.txt does not seem to contain an optimized query plan using indexes. Content: {content[:100]}..."