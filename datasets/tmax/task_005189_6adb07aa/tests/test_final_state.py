# test_final_state.py

import os
import json
import pytest

def test_metrics_json_exists_and_correct():
    """Check if metrics.json is generated and contains the correct non-leaky R2 score."""
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"File not found: {metrics_path}. Did you run the script?"

    with open(metrics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} does not contain valid JSON.")

    assert "mean_r2" in data, "metrics.json must contain the key 'mean_r2'."

    r2 = data["mean_r2"]
    assert isinstance(r2, (int, float)), "mean_r2 must be a number."

    # The true R2 without leakage is approx -0.1989
    assert r2 < 0.0, f"Expected negative R2 due to noise data without leakage, got {r2}. Data leakage might still be present."
    assert abs(r2 - (-0.1989)) < 0.05, f"Expected R2 around -0.1989, got {r2}. Did you use the correct model, k, and CV strategy?"

def test_pipeline_used_in_script():
    """Check if the script uses a Pipeline to prevent data leakage."""
    script_path = '/home/user/model_pipeline.py'
    assert os.path.isfile(script_path), f"File not found: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'Pipeline' in content or 'make_pipeline' in content, (
        "The script must use a Pipeline (or make_pipeline) from sklearn.pipeline to prevent data leakage."
    )

    # Check that the old leakage line is removed or commented out
    # "X_selected = selector.fit_transform(X, y)"
    # We won't strict-assert the exact line is missing just in case they modified it, 
    # but the pipeline usage and correct score are the main indicators.