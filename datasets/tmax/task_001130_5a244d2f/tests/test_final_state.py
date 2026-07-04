# test_final_state.py

import os
import subprocess
import pytest

def test_processor_c_exists():
    """Test that the C program source file exists."""
    c_file = "/home/user/processor.c"
    assert os.path.isfile(c_file), f"The file {c_file} is missing. You must write the C program."

def test_workflow_script_exists_and_executable():
    """Test that the workflow bash script exists and is executable."""
    script_file = "/home/user/workflow.sh"
    assert os.path.isfile(script_file), f"The file {script_file} is missing. You must write the bash script."
    assert os.access(script_file, os.X_OK), f"The script {script_file} is not executable. Run chmod +x on it."

def test_workflow_execution_and_output():
    """Test that running the workflow script produces the correct output."""
    script_file = "/home/user/workflow.sh"
    output_file = "/home/user/output.csv"
    expected_file = "/home/user/.expected_output.csv"

    # Execute the workflow script
    result = subprocess.run(
        [script_file],
        cwd="/home/user",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Execution of {script_file} failed with return code {result.returncode}.\n"
        f"Standard Error:\n{result.stderr}\n"
        f"Standard Output:\n{result.stdout}"
    )

    # Check that output file was created
    assert os.path.isfile(output_file), f"The output file {output_file} was not created by the workflow script."

    # Read and compare the contents
    with open(output_file, "r") as f_out:
        output_lines = [line.strip() for line in f_out if line.strip()]

    with open(expected_file, "r") as f_exp:
        expected_lines = [line.strip() for line in f_exp if line.strip()]

    assert len(output_lines) == len(expected_lines), (
        f"Row count mismatch: expected {len(expected_lines)} rows, but got {len(output_lines)} rows. "
        "Ensure filtering and inner join logic is correct."
    )

    for i, (out_line, exp_line) in enumerate(zip(output_lines, expected_lines)):
        assert out_line == exp_line, (
            f"Mismatch at row {i + 1}:\n"
            f"Expected: {exp_line}\n"
            f"Got:      {out_line}\n"
            "Check your regex filtering, join logic, math calculation, and output sorting/formatting."
        )