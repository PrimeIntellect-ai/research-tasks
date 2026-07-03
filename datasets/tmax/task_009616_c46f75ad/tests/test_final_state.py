# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

SCRIPT_PATH = "/home/user/extract_hierarchy.sh"

def test_script_exists_and_executable():
    """Test that the extract_hierarchy.sh script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script at {SCRIPT_PATH} is not executable."

def run_script_and_parse_json(*args):
    """Helper to run the script and parse its stdout as JSON."""
    result = subprocess.run(
        [SCRIPT_PATH] + [str(a) for a in args],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        pytest.fail(f"Script output is not valid JSON. Output was:\n{result.stdout}\nError: {e}")

    return data

def test_extract_hierarchy_case_1():
    """Test the script with MANAGER_ID=2, MIN_SALARY=90000, LIMIT=3."""
    data = run_script_and_parse_json(2, 90000, 3)

    expected = [
        {"id": 2, "name": "VP Eng", "salary": 150000},
        {"id": 4, "name": "Director Eng", "salary": 120000},
        {"id": 5, "name": "Eng Manager", "salary": 100000}
    ]

    assert data == expected, f"Expected {expected}, but got {data}"

def test_extract_hierarchy_case_2():
    """Test the script with MANAGER_ID=5, MIN_SALARY=60000, LIMIT=10."""
    data = run_script_and_parse_json(5, 60000, 10)

    expected = [
        {"id": 5, "name": "Eng Manager", "salary": 100000},
        {"id": 6, "name": "Senior Eng 1", "salary": 95000},
        {"id": 7, "name": "Senior Eng 2", "salary": 95000},
        {"id": 8, "name": "Junior Eng 1", "salary": 70000},
        {"id": 9, "name": "Junior Eng 2", "salary": 65000}
    ]

    assert data == expected, f"Expected {expected}, but got {data}"

def test_extract_hierarchy_empty_result():
    """Test the script with a high minimum salary that yields no results."""
    data = run_script_and_parse_json(5, 200000, 10)
    assert data == [], f"Expected empty list [], but got {data}"