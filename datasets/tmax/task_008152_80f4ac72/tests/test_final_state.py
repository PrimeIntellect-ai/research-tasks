# test_final_state.py

import os
import json
import pytest

def test_prepare_features_script_exists():
    script_path = "/home/user/prepare_features.py"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_features_json_exists():
    json_path = "/home/user/features.json"
    assert os.path.isfile(json_path), f"The output file {json_path} is missing."

def test_features_json_content():
    json_path = "/home/user/features.json"
    assert os.path.isfile(json_path), f"The output file {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_data = {
        "A": {
            "ca_count": 2,
            "length_diff_from_mean": -1.0
        },
        "B": {
            "ca_count": 3,
            "length_diff_from_mean": 2.0
        }
    }

    assert data == expected_data, f"The contents of {json_path} do not match the expected output. Got: {data}"

def test_features_json_keys_sorted():
    json_path = "/home/user/features.json"
    assert os.path.isfile(json_path), f"The output file {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    keys = list(data.keys())
    assert keys == sorted(keys), "The keys in the output JSON file are not sorted alphabetically."