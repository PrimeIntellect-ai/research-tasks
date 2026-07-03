# test_final_state.py

import os
import json
import pytest

def test_results_json_exists_and_correct():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Expected output file not found: {results_path}"

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON.")

    expected_data = [
        {
            "id": 4,
            "title": "Root2",
            "year": 2021,
            "total_citations": 3,
            "indirect_citations": []
        },
        {
            "id": 1,
            "title": "Root1",
            "year": 2020,
            "total_citations": 2,
            "indirect_citations": [
                "CitesRoot1_A_A",
                "CitesRoot1_A_B"
            ]
        }
    ]

    assert data == expected_data, f"The contents of {results_path} do not match the expected output."

def test_results_json_formatting():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Expected output file not found: {results_path}"

    with open(results_path, 'r') as f:
        content = f.read()

    # Check if it's likely indented with 2 spaces
    assert "\n  {" in content or "\n  \"" in content, "The JSON file does not appear to be formatted with 2-space indentation as required."