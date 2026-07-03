# test_final_state.py

import os
import json
import math
import pytest

def test_experiment_log_exists():
    log_path = "/home/user/output/experiment_log.json"
    assert os.path.isfile(log_path), f"Expected output file is missing: {log_path}"

def test_experiment_log_content():
    log_path = "/home/user/output/experiment_log.json"
    assert os.path.isfile(log_path), f"Expected output file is missing: {log_path}"

    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {log_path} does not contain valid JSON.")

    assert "valid_rows" in data, "JSON is missing the 'valid_rows' key."
    assert "avg_similarity" in data, "JSON is missing the 'avg_similarity' key."

    # Check valid_rows
    assert isinstance(data["valid_rows"], int), "'valid_rows' must be an integer."
    assert data["valid_rows"] == 4, f"Expected 4 valid_rows, got {data['valid_rows']}."

    # Check avg_similarity
    assert isinstance(data["avg_similarity"], (int, float)), "'avg_similarity' must be a number."
    expected_sim = 0.3841
    actual_sim = data["avg_similarity"]

    # Check if it's rounded to 4 decimal places and matches the expected value
    assert math.isclose(actual_sim, expected_sim, abs_tol=1e-4), \
        f"Expected avg_similarity to be approximately {expected_sim}, got {actual_sim}."