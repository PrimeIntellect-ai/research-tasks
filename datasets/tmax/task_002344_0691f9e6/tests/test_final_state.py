# test_final_state.py

import os
import json
import math

def test_embed_go_exists():
    """Check if the Go source file was created."""
    file_path = "/home/user/embed.go"
    assert os.path.exists(file_path), f"Go source file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_result_json_exists():
    """Check if the result JSON file was generated."""
    file_path = "/home/user/result.json"
    assert os.path.exists(file_path), f"Result file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_result_json_contents():
    """Validate the contents of the result JSON file."""
    file_path = "/home/user/result.json"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{file_path} does not contain valid JSON."

    assert "target_id" in data, "Result JSON is missing 'target_id' field."
    assert "similar_id" in data, "Result JSON is missing 'similar_id' field."
    assert "score" in data, "Result JSON is missing 'score' field."

    assert data["target_id"] == "doc4", f"Expected target_id to be 'doc4', got '{data['target_id']}'"
    assert data["similar_id"] == "doc1", f"Expected similar_id to be 'doc1', got '{data['similar_id']}'"

    # Check score with a small tolerance due to float rounding, though the spec says exactly 3 decimal places
    expected_score = 0.816
    assert math.isclose(data["score"], expected_score, abs_tol=0.001), \
        f"Expected score to be {expected_score}, got {data['score']}"