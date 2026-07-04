# test_final_state.py

import os
import json
import pytest

def test_metadata_report_exists_and_correct():
    report_path = "/home/user/metadata_report.json"

    assert os.path.exists(report_path), f"The expected output file {report_path} does not exist."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {report_path} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {report_path}: {e}")

    expected_data = {
        "/etc/passwd": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "/etc/hostname": "fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321",
        "/var/www/html/index.html": "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
        "/root/.bashrc": "cafebabecafebabecafebabecafebabecafebabecafebabecafebabecafebabe"
    }

    assert isinstance(data, dict), f"The JSON data in {report_path} should be a dictionary, but got {type(data).__name__}."

    # Check for missing or extra keys
    expected_keys = set(expected_data.keys())
    actual_keys = set(data.keys())

    missing_keys = expected_keys - actual_keys
    extra_keys = actual_keys - expected_keys

    assert not missing_keys, f"Missing expected file paths in the output: {missing_keys}"
    assert not extra_keys, f"Found unexpected file paths in the output: {extra_keys}"

    # Check values
    for key, expected_value in expected_data.items():
        actual_value = data[key]
        assert actual_value == expected_value, f"Checksum for {key} is incorrect. Expected '{expected_value}', got '{actual_value}'."