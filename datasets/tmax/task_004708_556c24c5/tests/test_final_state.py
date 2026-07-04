# test_final_state.py

import os
import json
import pytest

def test_region_summary_json_exists_and_correct():
    json_path = "/home/user/region_summary.json"
    assert os.path.isfile(json_path), f"Expected output file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, dict), "The JSON output should be a single JSON object (dictionary)."

    # Check expected values
    expected_values = {
        "East": 250,
        "North": 170,
        "South": 100
    }

    for region, expected_amount in expected_values.items():
        assert region in data, f"Region '{region}' is missing from the JSON output."
        actual_amount = data[region]
        assert isinstance(actual_amount, (int, float)), f"Value for '{region}' must be a number, not a string."
        assert actual_amount == expected_amount, f"Expected {expected_amount} for '{region}', but got {actual_amount}."

def test_analyze_script_tools():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read().lower()

    # Check that forbidden languages aren't used
    forbidden = ["python", "perl", "ruby", "node", "php"]
    for lang in forbidden:
        # A simple check to ensure they are not invoking these interpreters
        assert f"{lang} " not in content and f"/{lang}" not in content, \
            f"Script appears to use a forbidden language ({lang}). Only standard Linux command-line tools are allowed."