# test_final_state.py

import os
import pytest

def test_results_log_exists_and_format():
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. The task requires creating this file."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines (1 header, 4 features) in {log_path}, found {len(lines)}."
    assert lines[0] == "Feature,AbsDiff", f"Header in {log_path} is incorrect. Expected 'Feature,AbsDiff', got '{lines[0]}'."

    expected_diffs = {
        "A": 0.10,
        "C": 0.00,
        "G": 0.00,
        "T": 0.00
    }

    parsed_diffs = {}
    for line in lines[1:]:
        parts = line.split(",")
        assert len(parts) == 2, f"Line '{line}' is not in 'Feature,AbsDiff' format."
        feature, diff_str = parts
        try:
            diff = float(diff_str)
        except ValueError:
            pytest.fail(f"Value '{diff_str}' for feature '{feature}' is not a valid float.")
        parsed_diffs[feature] = diff

    for feature in ["A", "C", "G", "T"]:
        assert feature in parsed_diffs, f"Feature '{feature}' is missing from {log_path}."

    # Check values with tolerance (due to MCMC variance)
    tolerance = 0.05
    for feature, expected_val in expected_diffs.items():
        actual_val = parsed_diffs[feature]
        assert abs(actual_val - expected_val) <= tolerance, \
            f"AbsDiff for '{feature}' is {actual_val}, expected ~{expected_val} (within {tolerance})."