# test_final_state.py

import os
import json

def test_recommendations_file_exists():
    """Test that the recommendations file exists at the correct location."""
    file_path = "/home/user/recommendations.json"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

def test_recommendations_content():
    """Test that the recommendations file contains the correct expected JSON structure and values."""
    file_path = "/home/user/recommendations.json"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} does not contain valid JSON."

    expected_data = {
        "P001": ["P002", "P003", "P016"],
        "P005": ["P006", "P007", "P008"],
        "P009": ["P010", "P011", "P015"]
    }

    assert isinstance(data, dict), f"Expected JSON root to be a dictionary, got {type(data).__name__}."

    for key in expected_data:
        assert key in data, f"Target product ID '{key}' is missing from the recommendations."
        assert isinstance(data[key], list), f"Recommendations for '{key}' must be a list."
        assert data[key] == expected_data[key], f"Recommendations for '{key}' do not match. Expected {expected_data[key]}, got {data[key]}."

    assert len(data) == len(expected_data), f"Expected exactly {len(expected_data)} target products, but found {len(data)}."