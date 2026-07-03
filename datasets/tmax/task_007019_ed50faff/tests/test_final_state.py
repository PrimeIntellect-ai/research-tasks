# test_final_state.py
import os
import json
import pytest

RESULTS_FILE = '/home/user/results.json'

def test_results_file_exists():
    """Test that the results.json file was generated."""
    assert os.path.isfile(RESULTS_FILE), f"The file {RESULTS_FILE} was not found."

def test_results_format_and_values():
    """Test that results.json has the correct format and reasonable MCMC values."""
    assert os.path.isfile(RESULTS_FILE), f"The file {RESULTS_FILE} was not found."

    with open(RESULTS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_FILE} does not contain valid JSON.")

    expected_keys = {"posterior_mean", "acceptance_rate", "hypermutated"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

    post_mean = data["posterior_mean"]
    acc_rate = data["acceptance_rate"]
    hypermutated = data["hypermutated"]

    assert isinstance(post_mean, (int, float)), "posterior_mean must be a number."
    assert isinstance(acc_rate, (int, float)), "acceptance_rate must be a number."
    assert isinstance(hypermutated, bool), "hypermutated must be a boolean."

    # Analytical mean is 3.0. MCMC should be close.
    assert 2.8 <= post_mean <= 3.2, f"posterior_mean {post_mean} is out of expected bounds (2.8 - 3.2)."

    # Acceptance rate should be reasonable
    assert 0.1 <= acc_rate <= 0.9, f"acceptance_rate {acc_rate} is out of expected bounds (0.1 - 0.9)."

    # Hypermutated should be true since 3.0 > 2.5
    assert hypermutated is True, "hypermutated should be true since the posterior mean is > 2.5."