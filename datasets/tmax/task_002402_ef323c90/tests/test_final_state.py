# test_final_state.py

import os
import subprocess
import csv
import pytest

SCRIPT_PATH = "/home/user/run_query.sh"
CSV_PATH = "/home/user/materialized_graph.csv"

def test_script_exists_and_executable():
    """Check if the run_query.sh script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_script_produces_correct_csv():
    """Run the script and verify the resulting CSV matches the expected output exactly."""
    # Ensure we are testing the script's output, not a pre-existing file
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)

    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with exit code {result.returncode}. stderr: {result.stderr}"

    assert os.path.isfile(CSV_PATH), f"Output CSV not found at {CSV_PATH} after running the script"

    expected_csv = [
        ['id', 'root_id', 'depth', 'path_duration', 'rank_in_root'],
        ['1', '1', '0', '10', '6'],
        ['2', '1', '1', '15', '5'],
        ['3', '1', '1', '18', '3'],
        ['4', '1', '2', '18', '4'],
        ['5', '1', '2', '22', '1'],
        ['6', '6', '0', '15', '4'],
        ['7', '6', '1', '19', '3'],
        ['8', '6', '2', '25', '1'],
        ['9', '6', '1', '20', '2'],
        ['10', '1', '2', '20', '2']
    ]

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_csv = list(reader)

    assert actual_csv == expected_csv, "CSV contents do not match the expected schema or data."