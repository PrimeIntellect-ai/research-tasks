# test_final_state.py
import os
import json
import pytest

RESULT_PATH = "/home/user/path_result.json"

def test_result_file_exists():
    """Verify that the result JSON file exists."""
    assert os.path.exists(RESULT_PATH), f"Expected result file {RESULT_PATH} is missing."
    assert os.path.isfile(RESULT_PATH), f"{RESULT_PATH} is not a regular file."

def test_result_json_content():
    """Verify the content of the JSON file against the expected schema and values."""
    with open(RESULT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULT_PATH} does not contain valid JSON.")

    # Check for required keys
    assert "path" in data, "The JSON object is missing the required 'path' key."
    assert "distance" in data, "The JSON object is missing the required 'distance' key."

    # Verify no additional properties are present (as per additionalProperties: false)
    assert set(data.keys()) == {"path", "distance"}, f"The JSON object contains unexpected keys: {set(data.keys()) - {'path', 'distance'}}"

    # Expected values based on the graph filtering (>= 2010)
    expected_path = [
        "Dr. Alan Grant",
        "Dr. Ian Malcolm",
        "Dr. Henry Wu",
        "Dr. Ellie Sattler"
    ]
    expected_distance = 3

    # Validate path array
    assert isinstance(data["path"], list), "'path' must be an array."
    assert data["path"] == expected_path, f"Expected path {expected_path}, but got {data['path']}."

    # Validate distance integer
    assert isinstance(data["distance"], int), "'distance' must be an integer."
    assert data["distance"] == expected_distance, f"Expected distance {expected_distance}, but got {data['distance']}."