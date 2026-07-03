# test_final_state.py
import os
import json
import pytest
import math

def test_summary_json_exists():
    file_path = '/home/user/summary.json'
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_summary_json_content():
    file_path = '/home/user/summary.json'
    assert os.path.exists(file_path), f"Cannot verify content, {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {file_path} as JSON: {e}")

    # Expected keys
    expected_keys = {"total_valid_rows", "average_rating", "region_counts", "total_non_ascii_alnum"}
    assert set(data.keys()) == expected_keys, f"JSON keys mismatch. Expected {expected_keys}, got {set(data.keys())}."

    # Validate total_valid_rows
    assert data["total_valid_rows"] == 4, f"Expected total_valid_rows to be 4, got {data['total_valid_rows']}."

    # Validate average_rating
    avg_rating = data["average_rating"]
    assert isinstance(avg_rating, (int, float)), f"average_rating must be a number, got {type(avg_rating)}."
    assert math.isclose(avg_rating, 3.0, rel_tol=1e-9), f"Expected average_rating to be 3.0, got {avg_rating}."

    # Validate region_counts
    expected_region_counts = {"EU": 2, "NA": 1, "UNKNOWN": 1}
    assert data["region_counts"] == expected_region_counts, f"Expected region_counts to be {expected_region_counts}, got {data['region_counts']}."

    # Validate total_non_ascii_alnum
    assert data["total_non_ascii_alnum"] == 9, f"Expected total_non_ascii_alnum to be 9, got {data['total_non_ascii_alnum']}."