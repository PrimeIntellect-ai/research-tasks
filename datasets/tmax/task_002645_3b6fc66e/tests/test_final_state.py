# test_final_state.py

import os
import math
import pytest

def test_script_exists():
    """Verify that the integration script was created."""
    script_path = "/home/user/integrate_mpi.py"
    assert os.path.isfile(script_path), f"The script {script_path} was not created."

def test_output_file_exists():
    """Verify that the output file was created."""
    output_path = "/home/user/integration_output.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

def test_output_file_content():
    """Verify the contents of the output file."""
    output_path = "/home/user/integration_output.txt"
    with open(output_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 3, f"Expected exactly 3 lines in {output_path}, but found {len(lines)}."

    assert lines[0].startswith("Numerical: "), "First line must start with 'Numerical: '"
    assert lines[1].startswith("Analytical: "), "Second line must start with 'Analytical: '"
    assert lines[2].startswith("Error: "), "Third line must start with 'Error: '"

    try:
        numerical = float(lines[0].split("Numerical: ")[1])
        analytical = float(lines[1].split("Analytical: ")[1])
        error = float(lines[2].split("Error: ")[1])
    except ValueError as e:
        pytest.fail(f"Could not parse numerical values from the output file: {e}")

    # Check analytical value
    assert math.isclose(analytical, math.pi, rel_tol=1e-15), f"Analytical value {analytical} does not match math.pi."

    # Check numerical value (expected around 3.1415926535897643)
    expected_numerical = 3.1415926535897643
    assert math.isclose(numerical, expected_numerical, rel_tol=1e-12), f"Numerical value {numerical} is not close to expected {expected_numerical}."

    # Check error value
    expected_error = abs(expected_numerical - math.pi)
    assert math.isclose(error, expected_error, abs_tol=1e-12), f"Error value {error} is not correct."