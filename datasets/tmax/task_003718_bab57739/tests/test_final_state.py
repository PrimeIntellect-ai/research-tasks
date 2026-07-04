# test_final_state.py
import os
import json
import pytest

def test_final_metrics_exists():
    """Verify that the final output JSON file exists."""
    assert os.path.isfile('/home/user/final_metrics.json'), "The file /home/user/final_metrics.json does not exist."

def test_final_metrics_values():
    """Verify the estimated posterior mean and bootstrap confidence intervals."""
    with open('/home/user/final_metrics.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/final_metrics.json is not valid JSON.")

    assert 'posterior_mean' in data, "Missing 'posterior_mean' in final_metrics.json"
    assert 'ci_lower' in data, "Missing 'ci_lower' in final_metrics.json"
    assert 'ci_upper' in data, "Missing 'ci_upper' in final_metrics.json"

    mu_est = data['posterior_mean']
    ci_l = data['ci_lower']
    ci_u = data['ci_upper']

    assert isinstance(mu_est, (int, float)), "'posterior_mean' must be a number"
    assert isinstance(ci_l, (int, float)), "'ci_lower' must be a number"
    assert isinstance(ci_u, (int, float)), "'ci_upper' must be a number"

    # Target value from the true data generation process
    target_mu = 4.2
    error = abs(mu_est - target_mu)

    assert error <= 0.15, f"Metric threshold exceeded. Absolute error {error:.4f} > 0.15. Estimated mu: {mu_est}"
    assert ci_l <= target_mu <= ci_u, f"True mu ({target_mu}) is not within the bootstrap CI [{ci_l}, {ci_u}]"