# test_final_state.py

import json
import os
import pytest

RESULTS_PATH = "/home/user/results.json"

def test_results_file_exists():
    assert os.path.exists(RESULTS_PATH), f"The results file {RESULTS_PATH} does not exist."
    assert os.path.isfile(RESULTS_PATH), f"The path {RESULTS_PATH} is not a file."

def test_results_keys():
    with open(RESULTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON in {RESULTS_PATH}: {e}")

    required_keys = ["gamma", "omega", "noise_variance_ci_lower", "noise_variance_ci_upper"]
    for k in required_keys:
        assert k in data, f"Missing required key '{k}' in {RESULTS_PATH}."
        assert isinstance(data[k], (int, float)), f"Key '{k}' must be a float."

def test_parameter_accuracy():
    with open(RESULTS_PATH, "r") as f:
        data = json.load(f)

    true_gamma = 0.2
    true_omega = 3.14159

    gamma = data["gamma"]
    omega = data["omega"]

    err_gamma = abs(gamma - true_gamma)
    err_omega = abs(omega - true_omega)

    max_err = max(err_gamma, err_omega)

    assert max_err <= 0.05, (
        f"Parameter estimates exceed the tolerance threshold of 0.05. "
        f"Gamma error: {err_gamma:.4f} (estimated {gamma}, true {true_gamma}), "
        f"Omega error: {err_omega:.4f} (estimated {omega}, true {true_omega}), "
        f"Max error: {max_err:.4f}"
    )