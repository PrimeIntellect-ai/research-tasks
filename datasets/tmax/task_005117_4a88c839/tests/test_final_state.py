# test_final_state.py
import os
import pytest
import math

def test_kappa_estimate_accuracy():
    """
    Reads the student's estimated kappa from /home/user/kappa_estimate.txt
    and verifies that it is within 0.05 of the theoretical value (2.000).
    """
    output_path = "/home/user/kappa_estimate.txt"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content, f"File {output_path} is empty."

    try:
        estimated_kappa = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {output_path} as a float. Content: '{content}'")

    theoretical_kappa = 2.000
    error = abs(estimated_kappa - theoretical_kappa)
    threshold = 0.05

    assert error <= threshold, (
        f"Estimated kappa {estimated_kappa:.3f} is too far from the theoretical mode {theoretical_kappa:.3f}. "
        f"Absolute error: {error:.4f} (Threshold: <= {threshold})"
    )