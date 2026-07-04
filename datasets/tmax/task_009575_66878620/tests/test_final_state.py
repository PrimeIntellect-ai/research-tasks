# test_final_state.py

import os
import json
import pytest

RESULTS_PATH = '/home/user/results.json'
SCRIPT_PATH = '/home/user/process_and_train.py'

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_results_file_exists():
    assert os.path.isfile(RESULTS_PATH), f"The results file {RESULTS_PATH} does not exist."

def test_results_format_and_types():
    with open(RESULTS_PATH, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_PATH} does not contain valid JSON.")

    expected_keys = {
        "selected_features",
        "best_max_depth",
        "best_n_estimators",
        "best_cv_score"
    }

    actual_keys = set(results.keys())
    assert actual_keys == expected_keys, f"Expected keys {expected_keys}, but got {actual_keys}."

    # Check types and constraints
    assert isinstance(results["selected_features"], list), "selected_features must be a list."
    assert len(results["selected_features"]) == 3, "selected_features must contain exactly 3 features."

    # Features should be sorted alphabetically
    assert results["selected_features"] == sorted(results["selected_features"]), "selected_features must be sorted alphabetically."

    valid_features = {
        "cpu_usage", "memory_usage", "disk_io", 
        "network_in", "network_out", "cpu_mem_ratio"
    }
    for feature in results["selected_features"]:
        assert feature in valid_features, f"Unknown feature '{feature}' in selected_features."

    assert results["best_max_depth"] in [3, 5, None], "best_max_depth must be 3, 5, or null."
    assert results["best_n_estimators"] in [10, 50], "best_n_estimators must be 10 or 50."

    assert isinstance(results["best_cv_score"], (int, float)), "best_cv_score must be a number."

    # Check if best_cv_score is rounded to 4 decimal places
    score_str = str(results["best_cv_score"])
    if '.' in score_str:
        decimals = len(score_str.split('.')[1])
        assert decimals <= 4, f"best_cv_score must be rounded to 4 decimal places, got {decimals} decimal places."