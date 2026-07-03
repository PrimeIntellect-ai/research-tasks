# test_final_state.py

import os
import pytest

def test_result_file_exists():
    """Verify that the result file was created."""
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did the Rust program run and generate the output?"

def test_result_content():
    """Verify the content of the result file matches the expected calculations."""
    result_path = '/home/user/result.txt'
    if not os.path.isfile(result_path):
        pytest.fail(f"File {result_path} is missing.")

    with open(result_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "Result file does not contain enough lines."

    best_k_line = lines[0]
    assert best_k_line.startswith("Best K:"), f"Expected first line to start with 'Best K:', got '{best_k_line}'"

    # Extract K
    try:
        k_val = int(best_k_line.split(":")[1].strip())
    except ValueError:
        pytest.fail(f"Could not parse K from line: {best_k_line}")

    assert k_val == 2, f"Expected Best K to be 2, but got {k_val}"

    assert lines[1] == "Predictions:", f"Expected second line to be 'Predictions:', got '{lines[1]}'"

    expected_predictions = [
        "1,102,3.50",
        "3,101,3.50",
        "4,103,3.00"
    ]

    actual_predictions = lines[2:]

    assert len(actual_predictions) == len(expected_predictions), (
        f"Expected {len(expected_predictions)} predictions, but got {len(actual_predictions)}"
    )

    for expected, actual in zip(expected_predictions, actual_predictions):
        assert actual == expected, f"Expected prediction '{expected}', but got '{actual}'"