# test_final_state.py
import os
import pytest
import numpy as np

def test_final_result_accuracy():
    """
    Validates that the final computed energy in /home/user/final_result.txt
    is within a 5% relative error margin of the true sum of squares of the pulse amplitudes.
    """
    # Re-derive the ground truth expected energy based on the setup script logic
    np.random.seed(42)
    ground_truth_peaks = []
    for _ in range(50):
        amp = np.random.uniform(0.1, 1.0)
        ground_truth_peaks.append(amp)

    expected_energy = sum(p**2 for p in ground_truth_peaks)

    result_path = "/home/user/final_result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} was not found."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        actual_energy = float(content)
    except ValueError:
        pytest.fail(f"Could not parse a numerical float from {result_path}. Content: '{content}'")

    relative_error = abs(expected_energy - actual_energy) / expected_energy

    assert relative_error <= 0.05, (
        f"Relative error {relative_error:.4f} exceeds threshold of 0.05. "
        f"Expected approx {expected_energy:.4f}, but got {actual_energy:.4f}."
    )