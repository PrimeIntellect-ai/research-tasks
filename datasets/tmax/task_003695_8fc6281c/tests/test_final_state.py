# test_final_state.py

import os
import json
import pytest

def test_changepoint_json_exists():
    filepath = "/home/user/changepoint.json"
    assert os.path.isfile(filepath), f"Expected output file {filepath} does not exist."

def test_changepoint_json_content():
    filepath = "/home/user/changepoint.json"
    assert os.path.isfile(filepath), f"Expected output file {filepath} does not exist."

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} does not contain valid JSON.")

    expected_data = {
        "changepoint_date": "2023-10-08",
        "anomalous_value": 2500,
        "server_name": "WEB99"
    }

    assert data == expected_data, f"JSON content in {filepath} does not match the expected output. Got {data}"