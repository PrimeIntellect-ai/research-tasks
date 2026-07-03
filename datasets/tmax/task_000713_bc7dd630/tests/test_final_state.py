# test_final_state.py

import os
import json
import pytest

def test_token_counts_exists():
    file_path = "/home/user/token_counts.json"
    assert os.path.isfile(file_path), f"The required output file {file_path} is missing. Did your Go program run and generate it?"

def test_token_counts_content():
    file_path = "/home/user/token_counts.json"
    assert os.path.isfile(file_path), f"The required output file {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_data = {
        "AppAlpha": {
            "err 404 not found": 1,
            "login success us": 2,
            "logout user 123": 1,
            "no_action": 4
        },
        "AppBeta": {
            "err 500 timeout": 2,
            "login success eu": 1,
            "logout user 456": 1,
            "no_action": 4
        },
        "AppGamma": {
            "data load 100": 2,
            "no_action": 4,
            "sync complete": 2
        }
    }

    assert "AppAlpha" in data, "Missing 'AppAlpha' in the output JSON."
    assert "AppBeta" in data, "Missing 'AppBeta' in the output JSON."
    assert "AppGamma" in data, "Missing 'AppGamma' in the output JSON."

    assert data["AppAlpha"] == expected_data["AppAlpha"], f"AppAlpha counts are incorrect. Expected {expected_data['AppAlpha']}, got {data['AppAlpha']}"
    assert data["AppBeta"] == expected_data["AppBeta"], f"AppBeta counts are incorrect. Expected {expected_data['AppBeta']}, got {data['AppBeta']}"
    assert data["AppGamma"] == expected_data["AppGamma"], f"AppGamma counts are incorrect. Expected {expected_data['AppGamma']}, got {data['AppGamma']}"

    # Also verify that it's correctly formatted with 2-space indentation if possible, 
    # but the primary requirement is the logical correctness of the data.
    # We will just assert the parsed JSON matches exactly.
    assert data == expected_data, "The overall JSON output does not match the expected aggregation counts."