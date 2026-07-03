# test_final_state.py
import os
import json
import pytest

def test_pipeline_script_exists():
    """Verify that the pipeline.py script exists."""
    script_path = '/home/user/pipeline.py'
    assert os.path.exists(script_path), f"Script {script_path} does not exist. The task requires writing this script."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_model_results_json():
    """Verify that model_results.json exists and contains the correct structure and plausible values."""
    results_path = '/home/user/model_results.json'
    assert os.path.exists(results_path), f"Results file {results_path} does not exist. Did the script run successfully?"
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON.")

    assert "best_C" in results, "Key 'best_C' is missing from model_results.json."
    assert "best_score" in results, "Key 'best_score' is missing from model_results.json."

    best_c = results["best_C"]
    best_score = results["best_score"]

    assert isinstance(best_c, (int, float)), f"'best_C' must be a number, got {type(best_c).__name__}."
    assert best_c in [0.1, 1.0, 10.0], f"'best_C' must be one of the grid values [0.1, 1.0, 10.0], got {best_c}."

    assert isinstance(best_score, (int, float)), f"'best_score' must be a number, got {type(best_score).__name__}."
    assert 0.0 <= best_score <= 1.0, f"'best_score' must be between 0.0 and 1.0, got {best_score}."

    # Given the clear separation of clusters based on the synthetic words, the model should achieve very high accuracy
    assert best_score > 0.8, f"'best_score' should be high (> 0.8) given the dataset separation, but got {best_score}."