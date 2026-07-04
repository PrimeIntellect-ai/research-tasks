# test_final_state.py

import os
import json
import pytest

def test_metrics_json_exists_and_correct():
    """Check that metrics.json exists and contains the correct accuracy and inference_time."""
    metrics_path = "/home/user/metrics.json"
    assert os.path.isfile(metrics_path), f"The file {metrics_path} does not exist. Did you run the script?"

    with open(metrics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} is not valid JSON.")

    assert "accuracy" in data, "metrics.json is missing the 'accuracy' key."
    assert "inference_time" in data, "metrics.json is missing the 'inference_time' key."

    # The correct accuracy after fixing the leakage is 0.785
    expected_accuracy = 0.785
    actual_accuracy = data["accuracy"]
    assert abs(actual_accuracy - expected_accuracy) < 1e-5, \
        f"Expected accuracy to be approximately {expected_accuracy}, but got {actual_accuracy}. Data leakage might not be fixed correctly."

    actual_time = data["inference_time"]
    assert isinstance(actual_time, (int, float)) and actual_time >= 0, \
        f"Expected inference_time to be a non-negative number, got {actual_time}."

def test_evaluate_script_fixed():
    """Check that evaluate.py has been updated to fix the data leakage."""
    script_path = "/home/user/evaluate.py"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    # It should no longer fit_transform the entire X
    assert "scaler.fit_transform(X)" not in content, \
        "The script still contains `scaler.fit_transform(X)`. The data leakage is not fully fixed."

    # It should perform train_test_split on X, not X_scaled
    assert "train_test_split(X_scaled" not in content, \
        "The script still splits `X_scaled`. You must split `X` before scaling."