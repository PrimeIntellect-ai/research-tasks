# test_final_state.py

import os
import statistics
import pytest

def test_result_exists_and_correct():
    data_file = "/home/user/data.txt"
    result_file = "/home/user/result.txt"

    assert os.path.exists(data_file), "data.txt is missing. It should not have been modified or deleted."
    assert os.path.exists(result_file), "result.txt is missing. The script likely crashed or was not run."

    with open(data_file, 'r') as f:
        data = [float(line.strip()) for line in f if line.strip()]

    # Calculate the exact expected sample variance using Python's standard library
    # which uses a numerically stable algorithm.
    expected_var = statistics.variance(data)

    with open(result_file, 'r') as f:
        content = f.read().strip()

    try:
        actual_var = float(content)
    except ValueError:
        pytest.fail(f"result.txt does not contain a valid float: {content}")

    # Check if the computed variance matches the expected stable variance within 1e-5
    assert abs(actual_var - expected_var) < 1e-5, (
        f"Expected variance near {expected_var:.6f}, got {actual_var:.6f}. "
        "The script may still suffer from precision loss (catastrophic cancellation) "
        "or the variance formula is incorrect."
    )

def test_progress_log_exists_and_correct():
    progress_file = "/home/user/progress.log"
    assert os.path.exists(progress_file), "progress.log is missing. The script did not log progress."

    with open(progress_file, 'r') as f:
        lines = f.readlines()

    # The script processes 10000 lines, so there should be 10000 progress log entries.
    assert len(lines) == 10000, f"Expected exactly 10000 lines in progress.log, found {len(lines)}."