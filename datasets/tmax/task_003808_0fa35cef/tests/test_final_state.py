# test_final_state.py
import os
import json
import pytest

def test_artifact_exists():
    path = "/home/user/artifact.json"
    assert os.path.isfile(path), f"Expected artifact file {path} does not exist."

def test_artifact_content_and_schema():
    path = "/home/user/artifact.json"
    assert os.path.isfile(path), f"Expected artifact file {path} does not exist."

    with open(path, 'r') as f:
        try:
            artifact = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert isinstance(artifact, dict), "Artifact must be a JSON object (dictionary)."

    expected_keys = {"model", "best_alpha_1", "best_lambda_1", "cv_score"}
    actual_keys = set(artifact.keys())

    assert actual_keys == expected_keys, f"Artifact keys {actual_keys} do not exactly match expected keys {expected_keys}. No additional properties are allowed."

    assert artifact["model"] == "BayesianRidge", f"Expected model 'BayesianRidge', got {artifact['model']}."

    assert isinstance(artifact["best_alpha_1"], (int, float)), "best_alpha_1 must be a number."
    assert artifact["best_alpha_1"] in [1e-6, 1e-5, 1e-4], f"best_alpha_1 {artifact['best_alpha_1']} is not in the expected grid."

    assert isinstance(artifact["best_lambda_1"], (int, float)), "best_lambda_1 must be a number."
    assert artifact["best_lambda_1"] in [1e-6, 1e-5, 1e-4], f"best_lambda_1 {artifact['best_lambda_1']} is not in the expected grid."

    assert isinstance(artifact["cv_score"], (int, float)), "cv_score must be a number."
    assert 0.9 < artifact["cv_score"] <= 1.0, f"cv_score {artifact['cv_score']} is out of expected range (0.9, 1.0]."

def test_experiment_script_exists():
    path = "/home/user/experiment.py"
    assert os.path.isfile(path), f"Expected experiment script {path} does not exist."