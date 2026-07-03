# test_final_state.py

import os
import json
import math
import pytest

RECOMMENDATION_FILE = "/home/user/recommendation.json"

def test_recommendation_file_exists():
    assert os.path.isfile(RECOMMENDATION_FILE), f"Expected output file {RECOMMENDATION_FILE} does not exist."

def test_recommendation_content():
    try:
        with open(RECOMMENDATION_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {RECOMMENDATION_FILE} is not valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {RECOMMENDATION_FILE}: {e}")

    assert "most_similar_dataset" in data, "JSON missing 'most_similar_dataset' key."
    assert "cosine_similarity" in data, "JSON missing 'cosine_similarity' key."

    expected_dataset = "gamma.csv"
    actual_dataset = data["most_similar_dataset"]
    assert actual_dataset == expected_dataset, f"Expected most similar dataset to be '{expected_dataset}', but got '{actual_dataset}'."

    actual_similarity = data["cosine_similarity"]
    assert isinstance(actual_similarity, (int, float)), "Cosine similarity must be a number."
    assert 0.9990 <= actual_similarity <= 1.0000, f"Cosine similarity {actual_similarity} is out of expected bounds (0.9990 to 1.0000)."