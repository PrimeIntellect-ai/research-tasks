# test_final_state.py
import os
import json
import math

def test_best_params_exists():
    """Test that the best_params.json file was created."""
    file_path = "/home/user/best_params.json"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_best_params_format_and_values():
    """Test that the JSON file has the correct format and contains the expected optimal parameters."""
    file_path = "/home/user/best_params.json"
    with open(file_path, "r") as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    assert "gamma" in params, "Key 'gamma' is missing from best_params.json."
    assert "omega" in params, "Key 'omega' is missing from best_params.json."

    gamma = params["gamma"]
    omega = params["omega"]

    assert isinstance(gamma, (int, float)), f"Expected 'gamma' to be a float, got {type(gamma).__name__}."
    assert isinstance(omega, (int, float)), f"Expected 'omega' to be a float, got {type(omega).__name__}."

    # Based on the fixed seed of 42 and the specified uniform distributions,
    # the optimal parameters should be approximately gamma=0.8118 and omega=7.4813.
    # We use a tolerance to account for slight numerical differences in integration.
    expected_gamma = 0.8118
    expected_omega = 7.4813

    assert math.isclose(gamma, expected_gamma, abs_tol=0.05), \
        f"Expected gamma to be near {expected_gamma}, but got {gamma}. Check your random seed, sampling bounds, and cost function."
    assert math.isclose(omega, expected_omega, abs_tol=0.05), \
        f"Expected omega to be near {expected_omega}, but got {omega}. Check your random seed, sampling bounds, and cost function."