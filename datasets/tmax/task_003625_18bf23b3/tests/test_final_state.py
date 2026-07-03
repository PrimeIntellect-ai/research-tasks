# test_final_state.py

import os
import math
import pytest

def get_expected_stddev():
    """Derive the expected standard deviation based on the data loader logic."""
    # Data generation logic from loader.py
    data = [100000.0 + (i % 10) * 1e-5 for i in range(10000)]
    n = len(data)
    if n == 0:
        return 0.0

    # Calculate mean
    mean = sum(data) / n

    # Calculate variance using a stable two-pass method
    variance = sum((x - mean) ** 2 for x in data) / n

    return math.sqrt(variance)

def test_result_log_exists():
    """Verify that the script successfully ran and produced the result file."""
    assert os.path.isfile('/home/user/result.log'), (
        "The file /home/user/result.log was not found. "
        "Ensure that the monitor.py script executes successfully and writes the result."
    )

def test_result_log_value():
    """Verify that the calculated standard deviation is correct and does not suffer from precision loss."""
    with open('/home/user/result.log', 'r') as f:
        content = f.read().strip()

    assert content, "The file /home/user/result.log is empty."

    try:
        actual_stddev = float(content)
    except ValueError:
        pytest.fail(f"The content of /home/user/result.log is not a valid float: '{content}'")

    expected_stddev = get_expected_stddev()

    # The naive variance gives a negative number and crashes with math domain error on sqrt.
    # If they fixed it correctly, it should be very close to the expected stddev.
    assert math.isclose(actual_stddev, expected_stddev, rel_tol=1e-5), (
        f"The standard deviation in result.log ({actual_stddev}) does not match the expected value "
        f"({expected_stddev}). Ensure you implemented a numerically stable variance algorithm."
    )