# test_final_state.py

import os
import json
import pytest

def test_json_file_exists():
    """Check if the product_frequencies.json file was created."""
    json_path = "/home/user/product_frequencies.json"
    assert os.path.isfile(json_path), f"The file {json_path} does not exist."

def test_json_content_correct():
    """Check if the content of product_frequencies.json matches the expected frequencies."""
    json_path = "/home/user/product_frequencies.json"
    assert os.path.isfile(json_path), f"The file {json_path} does not exist."

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {json_path} as JSON: {e}")

    expected = {
        "AB-12345": 4,
        "XYZ-98765": 3,
        "ZZ-0000": 1,
        "RU-55555": 1
    }

    assert data == expected, f"JSON content does not match expected frequencies. Expected {expected}, got {data}"

def test_script_exists():
    """Check if the python script was created."""
    script_path = "/home/user/process_reviews.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."