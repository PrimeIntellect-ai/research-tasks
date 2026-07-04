# test_final_state.py
import os

def test_inflection_log():
    """Verify that the inflection.log file exists and contains the correct Cq value."""
    log_path = "/home/user/inflection.log"

    assert os.path.exists(log_path), f"Required output file is missing: {log_path}"
    assert os.path.isfile(log_path), f"Path exists but is not a regular file: {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_value = "22.5000"
    assert content == expected_value, f"Expected {log_path} to contain exactly '{expected_value}', but got '{content}'"