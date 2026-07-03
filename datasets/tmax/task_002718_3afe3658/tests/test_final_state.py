# test_final_state.py
import os
import json

def test_pipeline_results_json_exists():
    """Check if the pipeline_results.json file was generated."""
    file_path = "/home/user/pipeline_results.json"
    assert os.path.isfile(file_path), f"Expected results file not found at {file_path}"

def test_pipeline_results_content():
    """Validate the structure and content of the JSON results."""
    file_path = "/home/user/pipeline_results.json"
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    # Check required keys
    required_keys = {"selected_features", "best_alpha", "best_cv_mse"}
    assert required_keys.issubset(data.keys()), f"JSON missing required keys. Found: {list(data.keys())}"

    # Validate selected_features
    # Based on the deterministic setup:
    # sensor_A and sensor_A_roll3 are highly correlated (>0.85) -> drop sensor_A_roll3
    # sensor_B and sensor_C are highly correlated (>0.85) -> drop sensor_C
    # Remaining: sensor_A, sensor_B, sensor_B_roll3, sensor_D, sensor_E
    expected_features = ["sensor_A", "sensor_B", "sensor_B_roll3", "sensor_D", "sensor_E"]
    actual_features = data["selected_features"]

    assert isinstance(actual_features, list), "'selected_features' must be a list."
    assert actual_features == expected_features, (
        f"Expected selected_features to be exactly {expected_features} (alphabetical order), "
        f"but got {actual_features}."
    )

    # Validate best_alpha
    best_alpha = data["best_alpha"]
    valid_alphas = [0.1, 1.0, 10.0, 100.0]
    assert best_alpha in valid_alphas, f"'best_alpha' must be one of {valid_alphas}, got {best_alpha}"

    # Validate best_cv_mse
    best_cv_mse = data["best_cv_mse"]
    assert isinstance(best_cv_mse, float), f"'best_cv_mse' must be a float, got {type(best_cv_mse).__name__}"
    assert best_cv_mse > 0, f"'best_cv_mse' should be a positive mean squared error, got {best_cv_mse}"