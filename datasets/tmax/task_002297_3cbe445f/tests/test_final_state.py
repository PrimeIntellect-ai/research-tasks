# test_final_state.py

import os
import json
import pytest

def test_evaluate_rs_exists():
    rust_file = "/home/user/evaluate.rs"
    assert os.path.exists(rust_file), f"The Rust source file {rust_file} is missing."
    assert os.path.isfile(rust_file), f"The path {rust_file} is not a file."

def test_summary_json_exists_and_correct():
    json_file = "/home/user/summary.json"
    assert os.path.exists(json_file), f"The output file {json_file} is missing. Did you run your Rust program?"
    assert os.path.isfile(json_file), f"The path {json_file} is not a file."

    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_file} does not contain valid JSON.")

    assert "final_state" in data, "The JSON is missing the 'final_state' key."
    assert "score" in data, "The JSON is missing the 'score' key."

    assert data["final_state"] == "NODE_X", f"Expected final_state to be 'NODE_X', but got '{data['final_state']}'."
    assert data["score"] == 26, f"Expected score to be 26, but got {data['score']}."