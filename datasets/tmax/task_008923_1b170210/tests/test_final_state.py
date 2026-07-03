# test_final_state.py

import os
import json
import pytest

def test_access_path_exists_and_valid():
    output_path = "/home/user/access_path.json"

    assert os.path.isfile(output_path), f"Output file not found: {output_path}"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON")

    assert "path" in data, f"Key 'path' missing in {output_path}"
    assert "distance" in data, f"Key 'distance' missing in {output_path}"

    assert isinstance(data["path"], list), "'path' must be a list"
    assert isinstance(data["distance"], int), "'distance' must be an integer"

def test_access_path_correctness():
    output_path = "/home/user/access_path.json"

    if not os.path.isfile(output_path):
        pytest.skip("Output file does not exist, skipping correctness check.")

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Output file is not valid JSON, skipping correctness check.")

    expected_path = ["U_105", "Role_A", "Role_B", "R_992"]
    expected_distance = 3

    assert data["distance"] == expected_distance, f"Expected distance {expected_distance}, got {data.get('distance')}"
    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data.get('path')}"