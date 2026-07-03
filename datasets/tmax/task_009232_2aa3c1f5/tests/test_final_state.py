# test_final_state.py

import os
import subprocess
import pytest

def test_etl_script_exists_and_executable():
    """Check if the etl.sh script exists and is executable."""
    script_path = "/home/user/etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_etl_script_execution_and_output():
    """Run the etl.sh script and verify the summary.csv output."""
    script_path = "/home/user/etl.sh"
    output_path = "/home/user/summary.csv"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute. Error: {result.stderr}"

    # Check if output file exists
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    # Read the generated output
    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = """Region,TotalAmount
North,550.75
East,500.00
South,140.75
West,10.00"""

    # Compare lines to avoid newline issues at the end of file
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {output_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{content}"
    )