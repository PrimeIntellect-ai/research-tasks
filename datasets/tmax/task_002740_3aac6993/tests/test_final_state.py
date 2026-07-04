# test_final_state.py

import os
import json
import pytest

def test_fixed_daemon_exists():
    filepath = "/home/user/fixed_daemon.py"
    assert os.path.isfile(filepath), f"Expected fixed script at {filepath} is missing."

def test_final_state_json_exists():
    filepath = "/home/user/final_state.json"
    assert os.path.isfile(filepath), f"Expected output file at {filepath} is missing. Did you run the script and pipe the output?"

def test_final_state_values():
    filepath = "/home/user/final_state.json"
    assert os.path.isfile(filepath), "Cannot test values, final_state.json is missing."

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} does not contain valid JSON.")

    assert "s1" in data, "Key 's1' missing from final state JSON."
    assert "s2" in data, "Key 's2' missing from final state JSON."
    assert "s3" in data, "Key 's3' missing from final state JSON."

    # Compute expected values based on the rules and test data
    # s1: 00 (0), 02 (2), 01 (1) -> EMA: 0 -> 1.0 -> 1.0
    expected_s1 = 1.0
    # s2: ff (-1), fe (-2), fd (-3) -> EMA: -1 -> -1.5 -> -2.25
    expected_s2 = -2.25
    # s3: 7f (127), 80 (-128, diff > 50), 81 (-127, diff > 50) -> EMA: 127
    expected_s3 = 127.0

    assert abs(data["s1"] - expected_s1) < 0.01, f"Expected s1 to be near {expected_s1}, got {data['s1']}"
    assert abs(data["s2"] - expected_s2) < 0.01, f"Expected s2 to be near {expected_s2}, got {data['s2']}"
    assert abs(data["s3"] - expected_s3) < 0.01, f"Expected s3 to be near {expected_s3}, got {data['s3']}"