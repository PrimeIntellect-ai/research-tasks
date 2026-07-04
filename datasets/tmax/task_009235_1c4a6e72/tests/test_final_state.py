# test_final_state.py
import os
import json
import math
import pytest

def test_recommender_go_exists():
    file_path = "/home/user/recommender.go"
    assert os.path.isfile(file_path), f"The Go program {file_path} does not exist."

def test_results_json_exists_and_correct():
    file_path = "/home/user/results/run_exp_beta_01.json"
    assert os.path.isfile(file_path), f"The results file {file_path} does not exist. Did you run the program with the correct arguments?"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_run_id = "exp_beta_01"
    expected_target_id = 3
    expected_recommended_id = 1
    expected_score = 0.5

    assert "run_id" in data, "Key 'run_id' is missing from the JSON output."
    assert data["run_id"] == expected_run_id, f"Expected run_id '{expected_run_id}', but got '{data['run_id']}'."

    assert "target_id" in data, "Key 'target_id' is missing from the JSON output."
    assert data["target_id"] == expected_target_id, f"Expected target_id {expected_target_id}, but got {data['target_id']}."

    assert "recommended_id" in data, "Key 'recommended_id' is missing from the JSON output."
    assert data["recommended_id"] == expected_recommended_id, f"Expected recommended_id {expected_recommended_id}, but got {data['recommended_id']}."

    assert "similarity_score" in data, "Key 'similarity_score' is missing from the JSON output."
    assert isinstance(data["similarity_score"], (int, float)), "similarity_score must be a number."
    assert math.isclose(data["similarity_score"], expected_score, rel_tol=1e-5), f"Expected similarity_score {expected_score}, but got {data['similarity_score']}."