# test_final_state.py

import os
import pytest

def test_parser_exists():
    assert os.path.isfile("/home/user/parser.py"), "/home/user/parser.py is missing."

def test_run_all_script_exists():
    assert os.path.isfile("/home/user/run_all.sh"), "/home/user/run_all.sh is missing."

def test_results_log_exists():
    assert os.path.isfile("/home/user/results.log"), "/home/user/results.log is missing. Did you run run_all.sh?"

def test_results_log_content():
    expected_results = {
        "payload_a.swp": "VALID",
        "payload_b.swp": "INVALID_VERSION",
        "payload_c.swp": "REJECTED_INJECTION",
        "payload_d.swp": "INVALID_STATE",
        "payload_e.swp": "INVALID_VERSION",
        "payload_f.swp": "INVALID_STATE"
    }

    with open("/home/user/results.log", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    actual_results = {}
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            filename = parts[0].strip()
            result = parts[1].strip()
            actual_results[filename] = result

    for filename, expected_result in expected_results.items():
        assert filename in actual_results, f"Missing result for {filename} in /home/user/results.log"
        assert actual_results[filename] == expected_result, f"Expected {expected_result} for {filename}, but got {actual_results[filename]}"

    assert len(actual_results) == len(expected_results), f"Expected exactly {len(expected_results)} results, but found {len(actual_results)}."