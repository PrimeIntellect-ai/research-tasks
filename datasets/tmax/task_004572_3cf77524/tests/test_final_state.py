# test_final_state.py

import os
import json
import pytest

def test_rust_project_exists():
    assert os.path.isdir("/home/user/ms_analyzer"), "Rust project directory /home/user/ms_analyzer does not exist."
    assert os.path.isfile("/home/user/ms_analyzer/Cargo.toml"), "Cargo.toml not found in the Rust project directory."
    assert os.path.isfile("/home/user/ms_analyzer/src/main.rs"), "src/main.rs not found in the Rust project directory."

def test_result_json_exists_and_correct():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist. Did you run your Rust program?"

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON.")

    assert "KR_count" in data, "Key 'KR_count' missing from JSON output."
    assert "LLR" in data, "Key 'LLR' missing from JSON output."
    assert "Best_H" in data, "Key 'Best_H' missing from JSON output."

    assert data["KR_count"] == 4, f"Expected KR_count to be 4, but got {data['KR_count']}."

    # LLR calculation
    # N = 4, mu0 = 20.0, mu1 = 32.0, sigma = 15.0
    # x = [21.5, 19.8, 22.1, 18.5]
    # sum((x - mu1)^2) = 539.35
    # sum((x - mu0)^2) = 8.95
    # LLR = (539.35 - 8.95) / (2 * 15.0**2) = 530.4 / 450.0 = 1.178666...
    expected_llr = 1.179

    assert isinstance(data["LLR"], (int, float)), "LLR must be a number."
    assert abs(data["LLR"] - expected_llr) <= 0.001, f"Expected LLR to be approximately {expected_llr}, but got {data['LLR']}."

    assert data["Best_H"] == "H0", f"Expected Best_H to be 'H0', but got '{data['Best_H']}'."