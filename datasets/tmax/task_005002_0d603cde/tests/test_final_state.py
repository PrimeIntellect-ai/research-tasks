# test_final_state.py

import os
import json
import pytest

def test_rust_project_exists():
    project_dir = "/home/user/anomaly_detector"
    assert os.path.isdir(project_dir), f"The Rust project directory {project_dir} does not exist."

    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {project_dir}. Is it a valid Rust project?"

def test_anomalies_json_exists_and_valid():
    json_path = "/home/user/anomalies.json"
    assert os.path.isfile(json_path), f"The output file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {json_path} as JSON: {e}")

    assert isinstance(data, list), f"Expected the JSON root to be a list, but got {type(data).__name__}."
    for item in data:
        assert isinstance(item, str), f"Expected all items in the JSON array to be strings, but found {type(item).__name__}."

def test_anomalies_content():
    json_path = "/home/user/anomalies.json"
    if not os.path.isfile(json_path):
        pytest.fail(f"File {json_path} is missing.")

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {json_path}.")

    # The expected base IPs
    expected_base_ips = {"10.0.0.42", "10.1.2.3", "192.168.1.15", "8.8.8.8"}

    # The actual IPs found
    actual_ips = set(data)

    # Check that all base IPs are present
    missing_ips = expected_base_ips - actual_ips
    assert not missing_ips, f"The following expected IPs are missing from the output: {missing_ips}"

    # Check for unexpected IPs (allowing 256.256.256.256)
    allowed_extra_ips = {"256.256.256.256"}
    unexpected_ips = actual_ips - expected_base_ips - allowed_extra_ips
    assert not unexpected_ips, f"Found unexpected IPs in the output: {unexpected_ips}"

    # Check that the list is sorted alphabetically
    assert data == sorted(data), "The JSON array of IPs is not sorted alphabetically."