# test_final_state.py

import os
import math
import statistics
import pytest

def test_fixed_output_exists():
    """Check if the fixed_output.txt file was created."""
    output_file = "/home/user/fixed_output.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did you redirect the output?"

def test_fixed_output_values():
    """Verify that the output file contains the correct population variances."""
    csv_file = "/home/user/sensor_data.csv"
    output_file = "/home/user/fixed_output.txt"

    assert os.path.isfile(csv_file), f"Input file {csv_file} is missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    # Read the input data and calculate expected variances
    expected_variances = []
    with open(csv_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            values = [float(x) for x in line.split(',')]
            # Calculate population variance
            expected_var = statistics.pvariance(values)
            expected_variances.append(expected_var)

    # Read the actual output
    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_variances), (
        f"Expected {len(expected_variances)} lines of output, but found {len(actual_lines)}."
    )

    for i, (actual_str, expected_val) in enumerate(zip(actual_lines, expected_variances)):
        try:
            actual_val = float(actual_str)
        except ValueError:
            pytest.fail(f"Line {i+1} in {output_file} is not a valid float: '{actual_str}'")

        assert math.isclose(actual_val, expected_val, rel_tol=1e-5, abs_tol=1e-8), (
            f"Variance mismatch on line {i+1}: expected {expected_val}, got {actual_val}. "
            f"Make sure you are calculating the population variance using a numerically stable algorithm."
        )