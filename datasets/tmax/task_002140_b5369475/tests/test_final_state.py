# test_final_state.py

import os
import json
import pytest

def test_rust_project_exists():
    project_dir = "/home/user/temp_analyzer"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found at {cargo_toml}."

def test_summary_json_exists():
    summary_file = "/home/user/summary.json"
    assert os.path.isfile(summary_file), f"Summary JSON file {summary_file} does not exist."

def test_summary_json_content():
    summary_file = "/home/user/summary.json"

    with open(summary_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_file} does not contain valid JSON.")

    expected_keys = {"mean", "std_dev", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys {list(data.keys())} do not match expected {list(expected_keys)}."

    # Assert values with a small tolerance for rounding differences
    assert abs(data["mean"] - 46.05) <= 0.01, f"Expected mean ~46.05, got {data['mean']}"
    assert abs(data["std_dev"] - 1.37) <= 0.01, f"Expected std_dev ~1.37, got {data['std_dev']}"
    assert abs(data["ci_lower"] - 45.07) <= 0.01, f"Expected ci_lower ~45.07, got {data['ci_lower']}"
    assert abs(data["ci_upper"] - 47.03) <= 0.01, f"Expected ci_upper ~47.03, got {data['ci_upper']}"