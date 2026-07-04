# test_final_state.py

import os
import json
import math
import pytest

def test_recommendations_json_exists():
    """Test that the recommendations.json file exists."""
    file_path = "/home/user/recommendations.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The pipeline did not save the output correctly."

def test_recommendations_json_content():
    """Test that the recommendations.json file contains the correct top 3 recommendations."""
    file_path = "/home/user/recommendations.json"

    if not os.path.isfile(file_path):
        pytest.skip(f"{file_path} not found.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{file_path} is not a valid JSON file.")

    assert isinstance(data, list), f"Expected the JSON file to contain a list, but got {type(data).__name__}."
    assert len(data) == 3, f"Expected exactly 3 recommendations, but found {len(data)}."

    expected_results = [
        {"id": "train_3", "score": 0.3846},
        {"id": "train_1", "score": 0.2640},
        {"id": "train_5", "score": 0.1659}
    ]

    for i, (actual, expected) in enumerate(zip(data, expected_results)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary."
        assert "id" in actual, f"Item at index {i} is missing the 'id' key."
        assert "score" in actual, f"Item at index {i} is missing the 'score' key."

        assert actual["id"] == expected["id"], f"Expected id '{expected['id']}' at rank {i+1}, but got '{actual['id']}'."

        try:
            actual_score = float(actual["score"])
        except (ValueError, TypeError):
            pytest.fail(f"Score for item '{actual['id']}' is not a valid number: {actual['score']}")

        assert math.isclose(actual_score, expected["score"], abs_tol=0.0002), \
            f"Expected score {expected['score']} for id '{expected['id']}', but got {actual_score}."