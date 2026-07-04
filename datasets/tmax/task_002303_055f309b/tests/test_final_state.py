# test_final_state.py
import os
import json
import pytest

RESULTS_PATH = "/home/user/results.json"

def test_results_file_exists():
    assert os.path.exists(RESULTS_PATH), f"The expected output file {RESULTS_PATH} does not exist."
    assert os.path.isfile(RESULTS_PATH), f"{RESULTS_PATH} is not a file."

def test_results_content():
    with open(RESULTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output must be a list of objects."
    assert len(data) == 3, f"Expected exactly 3 authors in the results, got {len(data)}."

    expected_results = [
        {"author_name": "Bob", "score": 2.5, "rank": 1},
        {"author_name": "Alice", "score": 2.0, "rank": 2},
        {"author_name": "Charlie", "score": 1.0, "rank": 3}
    ]

    for i, expected in enumerate(expected_results):
        actual = data[i]
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        # Check keys
        expected_keys = {"author_name", "score", "rank"}
        actual_keys = set(actual.keys())
        assert actual_keys == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}."

        # Check values
        assert actual["author_name"] == expected["author_name"], f"Expected author_name '{expected['author_name']}' at rank {expected['rank']}, got '{actual['author_name']}'."
        assert isinstance(actual["score"], (int, float)), f"Score for {actual['author_name']} must be a float."
        assert float(actual["score"]) == expected["score"], f"Expected score {expected['score']} for {actual['author_name']}, got {actual['score']}."
        assert actual["rank"] == expected["rank"], f"Expected rank {expected['rank']} for {actual['author_name']}, got {actual['rank']}."