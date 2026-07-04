# test_final_state.py

import os
import subprocess
import csv
import pytest

SCRIPT_PATH = "/home/user/hierarchy_sales.py"
OUTPUT_PATH = "/home/user/output.csv"

def test_script_exists():
    """Check if the hierarchy_sales.py script exists."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."

def test_script_execution_and_output_3_1():
    """Run the script with limit 3 and offset 1, and verify the output."""
    # Run the script
    result = subprocess.run(
        ["python3", SCRIPT_PATH, "3", "1"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed to execute. Error:\n{result.stderr}"

    # Check if output file was created
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    # Read the output CSV
    with open(OUTPUT_PATH, "r", newline="") as f:
        reader = list(csv.reader(f))

    expected_output = [
        ["id", "name", "total_sales"],
        ["3", "Charlie", "10000"],
        ["2", "Bob", "8000"],
        ["6", "Frank", "6500"]
    ]

    assert reader == expected_output, f"Output CSV content is incorrect for limit 3, offset 1. Got: {reader}"

def test_script_execution_and_output_2_0():
    """Run the script with limit 2 and offset 0 to ensure pagination is dynamic."""
    result = subprocess.run(
        ["python3", SCRIPT_PATH, "2", "0"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed to execute. Error:\n{result.stderr}"

    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r", newline="") as f:
        reader = list(csv.reader(f))

    expected_output = [
        ["id", "name", "total_sales"],
        ["1", "Alice", "19000"],
        ["3", "Charlie", "10000"]
    ]

    assert reader == expected_output, f"Output CSV content is incorrect for limit 2, offset 0. Got: {reader}"