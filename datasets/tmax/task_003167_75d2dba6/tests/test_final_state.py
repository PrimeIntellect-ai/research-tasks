# test_final_state.py
import os
import re
import pytest

def test_analyze_backups_script_exists_and_executable():
    script_path = "/home/user/analyze_backups.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_user_storage_tsv_content():
    tsv_path = "/home/user/user_storage.tsv"
    assert os.path.isfile(tsv_path), f"The output file {tsv_path} does not exist. Did you run the script?"

    with open(tsv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Charlie\tEngineering\t10000",
        "Bob\tEngineering\t5512",
        "Alice\tHR\t3372"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {tsv_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."

def test_index_strategy_sql():
    sql_path = "/home/user/index_strategy.sql"
    assert os.path.isfile(sql_path), f"The file {sql_path} does not exist."

    with open(sql_path, "r") as f:
        content = f.read().strip()

    # Normalize whitespace and case
    normalized_content = re.sub(r'\s+', ' ', content).lower()

    # Check for the correct index creation
    # It must be a covering index for: WHERE department = ? AND status = 'active' ORDER BY name
    # So the index columns should be (department, status, name) or (status, department, name)

    assert "create index" in normalized_content, "The SQL statement must be a CREATE INDEX statement."
    assert "idx_dept_status_name" in normalized_content, "The index must be named 'idx_dept_status_name'."
    assert "on users" in normalized_content, "The index must be on the 'users' table."

    # Extract the column list
    match = re.search(r'\((.*?)\)', normalized_content)
    assert match is not None, "Could not find column list in parentheses."

    columns = [col.strip() for col in match.group(1).split(',')]
    assert len(columns) == 3, f"Expected exactly 3 columns in the index, found {len(columns)}."

    # The order of the first two columns (department, status) doesn't strictly matter for equality, 
    # but 'name' must be the last column to optimize the ORDER BY.
    assert set(columns[:2]) == {"department", "status"}, "The first two columns of the index must be 'department' and 'status' (in any order)."
    assert columns[2] == "name", "The third column of the index must be 'name' to optimize the ORDER BY clause."