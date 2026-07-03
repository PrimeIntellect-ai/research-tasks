# test_final_state.py
import os
import json
import pytest

def test_path_json_exists_and_correct():
    file_path = "/home/user/path.json"

    # Check if file exists
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

    # Read and parse JSON
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {file_path} does not contain valid JSON.")

    # Check structure and content
    assert "path" in data, f"The JSON in {file_path} is missing the 'path' key."
    assert isinstance(data["path"], list), f"The 'path' key in {file_path} must be a list."

    expected_path = ["P001", "P020", "P021", "P099"]
    actual_path = data["path"]

    assert actual_path == expected_path, (
        f"The computed path is incorrect. "
        f"Expected {expected_path}, but got {actual_path}."
    )