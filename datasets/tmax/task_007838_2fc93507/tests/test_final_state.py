# test_final_state.py

import os
import subprocess
import pytest

def test_optimize_sql_exists_and_correct():
    sql_path = "/home/user/optimize.sql"
    assert os.path.isfile(sql_path), f"File {sql_path} does not exist."

    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    assert "create index" in content, "optimize.sql does not contain a CREATE INDEX statement."
    assert "dependencies" in content, "optimize.sql does not reference the 'dependencies' table."
    assert "source" in content, "optimize.sql does not index the 'source' column."

def test_pathfinder_py_exists_and_parameterized():
    py_path = "/home/user/pathfinder.py"
    assert os.path.isfile(py_path), f"File {py_path} does not exist."

    with open(py_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for parameterized query usage (e.g., ?)
    assert "?" in content or ":" in content or "%s" in content, "pathfinder.py does not appear to use parameterized queries."

def test_pathfinder_execution():
    py_path = "/home/user/pathfinder.py"
    assert os.path.isfile(py_path), f"File {py_path} does not exist."

    # Run the script with arguments 15 and 85
    result = subprocess.run(
        ["python3", py_path, "15", "85"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"pathfinder.py failed to execute: {result.stderr}"
    output = result.stdout.strip()
    assert output == "15,33,71,85", f"pathfinder.py output incorrect. Expected '15,33,71,85', got '{output}'"

def test_path_txt_exists_and_correct():
    txt_path = "/home/user/path.txt"
    assert os.path.isfile(txt_path), f"File {txt_path} does not exist."

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == "15,33,71,85", f"path.txt content is incorrect. Expected '15,33,71,85', got '{content}'"