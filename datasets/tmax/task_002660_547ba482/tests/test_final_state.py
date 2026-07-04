# test_final_state.py

import os
import json
import math

def test_experiment_results_exist():
    output_path = "/home/user/experiment_results.json"
    assert os.path.isfile(output_path), f"Expected output file {output_path} is missing."

def test_experiment_results_format_and_values():
    output_path = "/home/user/experiment_results.json"
    with open(output_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {output_path} is not valid JSON."

    # Check keys
    expected_keys = {"accuracy_A", "accuracy_B", "p_value_ztest", "bayesian_posterior"}
    assert set(results.keys()) == expected_keys, f"JSON keys do not match expected. Found: {list(results.keys())}"

    # Check Model A deterministic values
    assert math.isclose(results["accuracy_A"], 0.8000, abs_tol=1e-4), \
        f"accuracy_A should be exactly 0.8000, got {results['accuracy_A']}"

    posterior = results["bayesian_posterior"]
    assert "model_A" in posterior and "model_B" in posterior, "bayesian_posterior missing model_A or model_B"

    model_A_post = posterior["model_A"]
    assert model_A_post.get("alpha") == 161, f"model_A alpha should be 161, got {model_A_post.get('alpha')}"
    assert model_A_post.get("beta") == 41, f"model_A beta should be 41, got {model_A_post.get('beta')}"

    # Check Model B structural invariants (N=200, uniform prior alpha=1, beta=1)
    model_B_post = posterior["model_B"]
    alpha_B = model_B_post.get("alpha")
    beta_B = model_B_post.get("beta")

    assert isinstance(alpha_B, int) and isinstance(beta_B, int), "Model B alpha and beta must be integers"
    assert alpha_B + beta_B == 202, f"Model B alpha + beta should equal 202 (200 samples + 2 prior), got {alpha_B + beta_B}"

    expected_acc_B = (alpha_B - 1) / 200.0
    assert math.isclose(results["accuracy_B"], expected_acc_B, abs_tol=1e-4), \
        f"accuracy_B ({results['accuracy_B']}) does not match the derived accuracy from alpha ({expected_acc_B})"

    # Check p-value
    p_val = results["p_value_ztest"]
    assert isinstance(p_val, (float, int)), "p_value_ztest must be a number"
    assert 0.0 <= p_val <= 1.0, f"p_value_ztest must be between 0 and 1, got {p_val}"