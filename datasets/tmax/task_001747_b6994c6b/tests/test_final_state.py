# test_final_state.py
import os
import json

def test_bootstrap_plot_generated():
    """Verify that the plot was successfully generated and is not empty."""
    plot_path = '/home/user/bootstrap_dist.png'
    assert os.path.isfile(plot_path), f"Plot file {plot_path} was not generated. The script might have crashed or the plotting backend is still misconfigured."
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} exists but is empty."

def test_metrics_json_generated_and_correct():
    """Verify that the metrics.json file contains the correct keys and correctly computed values."""
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} was not generated."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {metrics_path} does not contain valid JSON."

    expected_keys = {"bootstrap_mean", "ci_lower", "ci_upper", "model_mse"}
    actual_keys = set(metrics.keys())
    missing_keys = expected_keys - actual_keys
    assert not missing_keys, f"metrics.json is missing expected keys: {missing_keys}"

    ci_lower = metrics["ci_lower"]
    ci_upper = metrics["ci_upper"]
    model_mse = metrics["model_mse"]

    assert isinstance(ci_lower, (int, float)), "ci_lower must be a numeric value."
    assert isinstance(ci_upper, (int, float)), "ci_upper must be a numeric value."
    assert isinstance(model_mse, (int, float)), "model_mse must be a numeric value."

    # Check numerical accuracy based on the fixed script (replace=True, seed=42)
    assert abs(ci_lower - 37.1265) < 0.05, (
        f"ci_lower is incorrect. Expected ~37.1265, got {ci_lower}. "
        "Ensure you changed replace=False to replace=True in the np.random.choice call."
    )
    assert abs(ci_upper - 37.9100) < 0.05, (
        f"ci_upper is incorrect. Expected ~37.9100, got {ci_upper}. "
        "Ensure the bootstrap sampling logic is correct."
    )
    assert abs(model_mse - 1.0425) < 0.05, (
        f"model_mse is incorrect. Expected ~1.0425, got {model_mse}. "
        "Ensure the linear regression model is trained on the correct data."
    )