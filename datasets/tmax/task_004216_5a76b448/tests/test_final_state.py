# test_final_state.py

import os
import json
import pytest
import math

def test_rust_program_exists():
    # The prompt explicitly asks to write the Rust program at /home/user/prepare_data.rs
    # However, it also allows a Cargo project in /home/user/data_prep.
    # We check if either the standalone file exists or a main.rs inside data_prep exists.
    standalone_path = "/home/user/prepare_data.rs"
    cargo_path = "/home/user/data_prep/src/main.rs"

    assert os.path.isfile(standalone_path) or os.path.isfile(cargo_path), \
        "The Rust program was not found at /home/user/prepare_data.rs or /home/user/data_prep/src/main.rs"

def test_tracking_json_exists():
    json_path = "/home/user/tracking.json"
    assert os.path.isfile(json_path), f"The output file {json_path} does not exist."

def test_tracking_json_content():
    json_path = "/home/user/tracking.json"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert "total_tokens" in data, "Missing 'total_tokens' in JSON output."
    assert "anomaly_count" in data, "Missing 'anomaly_count' in JSON output."
    assert "posterior_expected_value" in data, "Missing 'posterior_expected_value' in JSON output."

    # Check the derived values
    assert data["total_tokens"] == 16, f"Expected total_tokens to be 16, got {data['total_tokens']}"
    assert data["anomaly_count"] == 3, f"Expected anomaly_count to be 3, got {data['anomaly_count']}"

    expected_posterior = 0.25
    assert math.isclose(data["posterior_expected_value"], expected_posterior, rel_tol=1e-4), \
        f"Expected posterior_expected_value to be ~{expected_posterior}, got {data['posterior_expected_value']}"