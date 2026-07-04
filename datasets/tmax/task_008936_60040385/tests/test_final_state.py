# test_final_state.py

import os
import json

def test_changepoints_json_exists():
    """Test that the changepoints.json file exists."""
    file_path = "/home/user/changepoints.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The task requires creating this file."

def test_changepoints_json_content():
    """Test that the changepoints.json contains the correct dates."""
    file_path = "/home/user/changepoints.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} does not contain valid JSON."

    expected = ["2023-10-04", "2023-10-08"]
    assert isinstance(data, list), "The JSON content should be a list of strings."
    assert data == expected, f"Expected changepoints {expected}, but got {data}."