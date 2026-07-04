# test_final_state.py

import os
import json
import pytest

def test_solution_rs_exists():
    path = "/home/user/solution.rs"
    assert os.path.isfile(path), f"File {path} does not exist. The task requires writing a Rust program here."

def test_result_json_exists_and_correct():
    path = "/home/user/result.json"
    assert os.path.isfile(path), f"File {path} does not exist. Did you redirect the output of your Rust program?"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert isinstance(data, dict), f"File {path} should contain a JSON object."

    assert "cwe" in data, f"Key 'cwe' missing in {path}."
    assert "blocked_ip" in data, f"Key 'blocked_ip' missing in {path}."

    expected_cwe = "CWE-22"
    expected_ip = "172.16.0.42"

    assert data["cwe"] == expected_cwe, f"Expected 'cwe' to be '{expected_cwe}', but got '{data['cwe']}'."
    assert data["blocked_ip"] == expected_ip, f"Expected 'blocked_ip' to be '{expected_ip}', but got '{data['blocked_ip']}'."