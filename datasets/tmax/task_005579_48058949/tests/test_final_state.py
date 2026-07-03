# test_final_state.py
import os
import json

def test_experiment_json_exists_and_valid():
    """Verify that experiment.json exists and contains the correct structure and types."""
    json_path = '/home/user/experiment.json'
    assert os.path.isfile(json_path), f"Expected results file missing at {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    expected_keys = {"best_alpha", "mean_cv_r2_original", "bootstrap_se_r2"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, but got {set(data.keys())}"

    # Check types and valid ranges
    assert isinstance(data["best_alpha"], (int, float)), "best_alpha must be a number"
    assert data["best_alpha"] in [0.1, 1.0, 10.0], f"best_alpha must be one of [0.1, 1.0, 10.0], got {data['best_alpha']}"

    assert isinstance(data["mean_cv_r2_original"], (int, float)), "mean_cv_r2_original must be a number"
    assert -1.0 <= data["mean_cv_r2_original"] <= 1.0, "mean_cv_r2_original should be an R-squared value"

    assert isinstance(data["bootstrap_se_r2"], (int, float)), "bootstrap_se_r2 must be a number"
    assert data["bootstrap_se_r2"] >= 0.0, "bootstrap_se_r2 must be non-negative"