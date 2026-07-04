# test_final_state.py

import os
import pytest

def test_script_exists():
    """Check that the script was created."""
    script_file = "/home/user/perf_profile/analyze_step.py"
    assert os.path.exists(script_file), f"Script file {script_file} was not found."

def test_output_file_exists():
    """Check that the output file was created."""
    output_file = "/home/user/perf_profile/optimal_dt.txt"
    assert os.path.exists(output_file), f"Output file {output_file} was not found."

def test_optimal_dt_value():
    """Check that the optimal dt value is correct."""
    output_file = "/home/user/perf_profile/optimal_dt.txt"
    assert os.path.exists(output_file), f"Output file {output_file} was not found."

    with open(output_file, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as a float.")

    assert val == 0.02, f"Expected optimal dt to be 0.02, but got {val}."