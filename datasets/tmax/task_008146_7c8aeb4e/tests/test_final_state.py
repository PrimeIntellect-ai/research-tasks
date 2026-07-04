# test_final_state.py
import os
import math

def test_integral_result_exists_and_format():
    """Verify that the integral result file exists and is formatted correctly."""
    path = "/home/user/integral_result.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a regular file."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {path} is empty."

    # Check if it's formatted to exactly 12 decimal places
    assert "." in content, "Result must contain a decimal point."
    parts = content.split(".")
    assert len(parts) == 2, "Result must contain exactly one decimal point."
    assert len(parts[1]) == 12, f"Result must be formatted to exactly 12 decimal places, found {len(parts[1])}."

    try:
        val = float(content)
    except ValueError:
        assert False, f"Result '{content}' is not a valid float."

    # The expected value based on the fixed random seed in setup is ~0.999917520038
    # We check if it is reasonably close to ensure the computation was performed correctly.
    expected = 0.999917520038
    assert math.isclose(val, expected, abs_tol=1e-7), \
        f"Calculated integral {val} is not correct. Expected roughly {expected}."