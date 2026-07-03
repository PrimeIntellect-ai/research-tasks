# test_final_state.py
import os
import json
import pytest

OUTPUT_PATH = "/home/user/output/top_terms.json"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."

def test_output_is_valid_json():
    with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {OUTPUT_PATH} is not valid JSON.")
    assert isinstance(data, dict), "Output JSON must be a dictionary."

def test_output_content():
    with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    expected_keys = {"Electronics", "Clothing", "Home"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, but got {set(data.keys())}."

    expected_electronics = ["amazing", "picture", "bad", "battery", "great"]
    expected_clothing = ["color", "cotton", "fit", "fits", "great"]
    expected_home = ["adore", "bien", "j", "kaufen", "müll"]

    assert data["Electronics"] == expected_electronics, f"Expected Electronics to be {expected_electronics}, got {data['Electronics']}"
    assert data["Clothing"] == expected_clothing, f"Expected Clothing to be {expected_clothing}, got {data['Clothing']}"
    assert data["Home"] == expected_home, f"Expected Home to be {expected_home}, got {data['Home']}"