# test_final_state.py

import os
import json
import pytest

CLEAN_DIR = "/home/user/dataset_clean"
ORIGINAL_DIR = "/home/user/dataset"

def test_clean_directory_exists():
    assert os.path.isdir(CLEAN_DIR), f"Directory {CLEAN_DIR} does not exist."

def test_catalog_json_exists_and_correct():
    catalog_path = os.path.join(CLEAN_DIR, "catalog.json")
    assert os.path.isfile(catalog_path), f"Catalog file {catalog_path} does not exist."

    with open(catalog_path, "r", encoding="utf-8") as f:
        try:
            catalog = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {catalog_path} is not valid JSON.")

    expected_catalog = {
        "EXP-X99": {"operator": "Dr.Smith", "max_z": 12.4, "original_prefix": "001"},
        "EXP-Y42": {"operator": "Alice", "max_z": 22.1, "original_prefix": "002"},
        "EXP-Z01": {"operator": "Bob", "max_z": 8.5, "original_prefix": "003"}
    }

    assert isinstance(catalog, dict), "Catalog must be a JSON object (dictionary)."

    for exp_id, expected_data in expected_catalog.items():
        assert exp_id in catalog, f"Expected experiment ID '{exp_id}' missing from catalog."
        actual_data = catalog[exp_id]

        assert "operator" in actual_data, f"Missing 'operator' in catalog for {exp_id}."
        assert actual_data["operator"] == expected_data["operator"], f"Incorrect operator for {exp_id}."

        assert "max_z" in actual_data, f"Missing 'max_z' in catalog for {exp_id}."
        assert isinstance(actual_data["max_z"], (int, float)), f"'max_z' for {exp_id} must be a number."
        assert abs(actual_data["max_z"] - expected_data["max_z"]) < 1e-6, f"Incorrect max_z for {exp_id}. Expected {expected_data['max_z']}, got {actual_data['max_z']}."

        assert "original_prefix" in actual_data, f"Missing 'original_prefix' in catalog for {exp_id}."
        assert actual_data["original_prefix"] == expected_data["original_prefix"], f"Incorrect original_prefix for {exp_id}."

@pytest.mark.parametrize("original_prefix, expected_filename", [
    ("001", "EXP-X99_Dr.Smith.csv"),
    ("002", "EXP-Y42_Alice.csv"),
    ("003", "EXP-Z01_Bob.csv")
])
def test_csv_files_copied_and_renamed(original_prefix, expected_filename):
    clean_csv_path = os.path.join(CLEAN_DIR, expected_filename)
    original_csv_path = os.path.join(ORIGINAL_DIR, f"data_{original_prefix}.csv")

    assert os.path.isfile(clean_csv_path), f"Expected CSV file {clean_csv_path} does not exist."
    assert os.path.isfile(original_csv_path), f"Original CSV file {original_csv_path} does not exist (was it deleted?)."

    with open(clean_csv_path, "r", encoding="utf-8") as f:
        clean_content = f.read()
    with open(original_csv_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    assert clean_content == original_content, f"Content of {clean_csv_path} does not match the original {original_csv_path}."