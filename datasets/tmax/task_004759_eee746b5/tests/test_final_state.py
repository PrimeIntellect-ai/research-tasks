# test_final_state.py

import os
import stat
import json
import sqlite3
import subprocess
import pytest

def test_script_exists_and_executable():
    """Test that the script exists and is executable."""
    script_path = "/home/user/run_analysis.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_run_script():
    """Run the script to ensure it executes without errors."""
    script_path = "/home/user/run_analysis.sh"
    # We execute the script to generate or regenerate the outputs
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_database_exists_and_valid():
    """Test that the SQLite database was created and is a valid SQLite file."""
    db_path = "/home/user/company.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    # Check if it's a valid SQLite database by connecting and running a simple pragma
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        conn.close()
        assert result and result[0] == "ok", "Database integrity check failed."
    except sqlite3.Error as e:
        pytest.fail(f"Failed to connect to SQLite database {db_path}: {e}")

def test_json_output():
    """Test that the JSON output exactly matches the expected cross-departmental anomalies."""
    json_path = "/home/user/cross_dept_analysis.json"
    assert os.path.isfile(json_path), f"JSON output {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected = [
        {
            "employee": "Bob",
            "employee_dept": "Engineering",
            "project": "Gamma",
            "project_dept": "Exec",
            "management_depth": 1
        },
        {
            "employee": "Charlie",
            "employee_dept": "Engineering",
            "project": "Beta",
            "project_dept": "Sales",
            "management_depth": 2
        },
        {
            "employee": "Dave",
            "employee_dept": "Sales",
            "project": "Alpha",
            "project_dept": "Engineering",
            "management_depth": 2
        }
    ]

    assert isinstance(data, list), "JSON output should be a list of objects."
    assert len(data) == len(expected), f"Expected {len(expected)} records, but got {len(data)}."

    # The prompt requires sorting by employee name, then by project name.
    # The expected list is already sorted this way.
    assert data == expected, f"JSON output does not match the expected cross-departmental analysis.\nExpected: {expected}\nGot: {data}"