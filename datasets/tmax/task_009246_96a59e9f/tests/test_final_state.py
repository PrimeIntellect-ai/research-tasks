# test_final_state.py

import os
import json
import pytest

def test_results_json_exists_and_format():
    results_path = "/home/user/experiments/results.json"
    assert os.path.isfile(results_path), f"File {results_path} is missing."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not a valid JSON file.")

    assert isinstance(results, list), f"{results_path} should contain a list of dictionaries."
    assert len(results) == 4, f"{results_path} should have exactly 4 entries for the grid search."

    expected_combinations = [
        {"n_estimators": 10, "max_depth": 3},
        {"n_estimators": 50, "max_depth": 3},
        {"n_estimators": 10, "max_depth": 5},
        {"n_estimators": 50, "max_depth": 5}
    ]

    found_combinations = []
    for entry in results:
        assert isinstance(entry, dict), "Each entry in results.json must be a dictionary."
        assert "n_estimators" in entry, "Missing 'n_estimators' in results entry."
        assert "max_depth" in entry, "Missing 'max_depth' in results entry."
        assert "mean_accuracy" in entry, "Missing 'mean_accuracy' in results entry."

        assert isinstance(entry["mean_accuracy"], float), "'mean_accuracy' must be a float."

        found_combinations.append({
            "n_estimators": entry["n_estimators"],
            "max_depth": entry["max_depth"]
        })

    for combo in expected_combinations:
        assert combo in found_combinations, f"Missing grid search combination {combo} in results.json."

def test_best_params_json_exists_and_format():
    best_params_path = "/home/user/experiments/best_params.json"
    assert os.path.isfile(best_params_path), f"File {best_params_path} is missing."

    with open(best_params_path, "r") as f:
        try:
            best_params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{best_params_path} is not a valid JSON file.")

    assert isinstance(best_params, dict), f"{best_params_path} should contain a dictionary."
    assert "n_estimators" in best_params, "Missing 'n_estimators' in best_params.json."
    assert "max_depth" in best_params, "Missing 'max_depth' in best_params.json."

    assert best_params["n_estimators"] in [10, 50], "'n_estimators' should be either 10 or 50."
    assert best_params["max_depth"] in [3, 5], "'max_depth' should be either 3 or 5."

def test_pipeline_script_modifications():
    pipeline_path = "/home/user/scripts/pipeline.py"
    assert os.path.isfile(pipeline_path), f"Script {pipeline_path} is missing."

    with open(pipeline_path, "r") as f:
        content = f.read()

    # Check if the missing values were filled with -1
    assert "-1" in content, "The script does not seem to fill missing values with -1."

    # Check if the column was cast to int
    assert "int" in content, "The script does not seem to cast the column to integer."

    # Check if GridSearchCV and random_state are used
    assert "GridSearchCV" in content, "GridSearchCV is not used in the script."
    assert "42" in content, "random_state=42 does not seem to be set."