# test_final_state.py

import os
import subprocess
import pytest

def test_analyze_script_exists():
    """Check if the analyze script exists."""
    script_path = '/home/user/analyze.sh'
    assert os.path.isfile(script_path), f"Script not found: {script_path}"

def test_analyze_script_execution_and_output():
    """Run the analyze script and verify the output file contents."""
    script_path = '/home/user/analyze.sh'
    output_path = '/home/user/priors.tsv'

    # Run the script
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error:\n{result.stderr}"

    # Verify the output file exists
    assert os.path.isfile(output_path), f"Output file not found: {output_path}"

    # Verify the contents of the output file
    expected_content = "alpha\t0.5926\nbeta\t0.3438\ngamma\t0.4815\n"

    with open(output_path, 'r') as f:
        actual_content = f.read()

    # Strip trailing newlines for a more robust comparison, but ensure the structure matches
    expected_lines = [line.strip() for line in expected_content.strip().split('\n')]
    actual_lines = [line.strip() for line in actual_content.strip().split('\n')]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, got {len(actual_lines)}"

    for expected, actual in zip(expected_lines, actual_lines):
        assert actual == expected, f"Expected line '{expected}', but got '{actual}'"