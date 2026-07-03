# test_final_state.py

import os
import json
import pytest

def test_processed_json_exists_and_correct():
    processed_path = "/home/user/processed.json"
    assert os.path.isfile(processed_path), f"The file {processed_path} was not created. Did the script run successfully?"

    try:
        with open(processed_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {processed_path} does not contain valid JSON.")

    expected_data = {
        "event": "login",
        "payload": {
            "nested": "Hello"
        },
        "metadata": "not_json_string",
        "status": "success"
    }

    assert data == expected_data, (
        f"The content of {processed_path} does not match the expected normalized telemetry. "
        f"Expected: {expected_data}, but got: {data}"
    )