# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/analyze_graph.sh"
DB_PATH = "/home/user/routing.db"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    # Run the script with arguments "Alpha" and 3
    result = subprocess.run(
        [SCRIPT_PATH, "Alpha", "3"],
        capture_output=True,
        text=True,
        cwd="/home/user"
    )

    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    output = result.stdout.strip().replace("\r\n", "\n")
    expected_output = (
        "destination_name,min_total_weight,rank\n"
        "Bravo,10,1\n"
        "Charlie,15,2\n"
        "Delta,20,3\n"
        "Echo,30,4"
    )

    assert output == expected_output, f"Script output did not match expected.\nExpected:\n{expected_output}\nGot:\n{output}"

def test_database_created():
    # The script should have created the SQLite database
    assert os.path.isfile(DB_PATH), f"Database {DB_PATH} was not created."

    # Verify the database contains the imported tables
    result = subprocess.run(
        ["sqlite3", DB_PATH, "SELECT name FROM sqlite_master WHERE type='table';"],
        capture_output=True,
        text=True
    )
    tables = result.stdout.strip().split("\n")
    assert "nodes" in tables, "Table 'nodes' not found in the database."
    assert "edges" in tables, "Table 'edges' not found in the database."