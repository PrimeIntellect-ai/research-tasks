# test_final_state.py

import json
import os
import sqlite3

def test_final_output_exists_and_valid():
    output_path = "/home/user/top_authors.json"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "Output is not valid JSON."

    assert isinstance(data, list), "Output must be a JSON array."

    # Expected values derived from the dataset
    expected_peak_decades = {
        "Alice": 1990,
        "Bob": 2000,
        "Charlie": 2010,
        "Diana": 2010,
        "Eve": 2020
    }

    expected_coauthor_weights = {
        "Alice": 1,
        "Bob": 1,
        "Charlie": 1,
        "Diana": 1,
        "Eve": 1
    }

    required_keys = {"author_id", "author_name", "peak_decade", "author_score", "decade_rank", "max_coauthor_weight"}

    authors_found = set()

    for item in data:
        assert isinstance(item, dict), "Each item in the array must be a JSON object."
        missing_keys = required_keys - set(item.keys())
        assert not missing_keys, f"Missing keys in output object: {missing_keys}"

        name = item["author_name"]
        authors_found.add(name)

        assert name in expected_peak_decades, f"Unexpected author found: {name}"
        assert item["peak_decade"] == expected_peak_decades[name], \
            f"Wrong peak decade for {name}. Expected {expected_peak_decades[name]}, got {item['peak_decade']}."

        assert item["max_coauthor_weight"] == expected_coauthor_weights[name], \
            f"Wrong max coauthor weight for {name}. Expected {expected_coauthor_weights[name]}, got {item['max_coauthor_weight']}."

        assert isinstance(item["author_score"], (int, float)), f"author_score for {name} must be a number."
        assert isinstance(item["decade_rank"], int), f"decade_rank for {name} must be an integer."
        assert 1 <= item["decade_rank"] <= 3, f"decade_rank for {name} must be between 1 and 3."

    # Verify all expected authors are present in the output
    missing_authors = set(expected_peak_decades.keys()) - authors_found
    assert not missing_authors, f"Missing authors in the final output: {missing_authors}"