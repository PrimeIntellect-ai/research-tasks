# test_final_state.py
import os
import json

def test_results_json_structure_and_values():
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"File {results_path} is missing. The pipeline did not produce the expected output file."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not valid JSON."

    expected_models = {
        "Q1": "A",
        "Q2": "B",
        "Q3": "B",
        "Q4": "A"
    }

    for q, expected_model in expected_models.items():
        assert q in results, f"Quadrant {q} is missing from the results JSON."
        assert "best_model" in results[q], f"'best_model' key is missing in quadrant {q}."
        assert "mse" in results[q], f"'mse' key is missing in quadrant {q}."

        actual_model = results[q]["best_model"]
        assert actual_model == expected_model, (
            f"Expected best_model for {q} to be '{expected_model}', but got '{actual_model}'. "
            "Check your domain decomposition and optimization logic."
        )

        mse = results[q]["mse"]
        assert isinstance(mse, (int, float)), f"MSE for {q} must be a numeric value, got {type(mse).__name__}."
        assert 0.0 < mse < 1.0, f"MSE for {q} ({mse}) is outside the expected reasonable bounds. It should be small but positive."