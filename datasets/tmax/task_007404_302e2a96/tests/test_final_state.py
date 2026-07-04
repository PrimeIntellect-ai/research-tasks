# test_final_state.py
import os
import json
import pytest

def test_results_json_exists():
    file_path = "/home/user/results.json"
    assert os.path.exists(file_path), f"File missing: {file_path}"
    assert os.path.isfile(file_path), f"Not a file: {file_path}"

def test_results_content():
    file_path = "/home/user/results.json"
    assert os.path.exists(file_path), f"File missing: {file_path}"

    with open(file_path, 'r') as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_keys = {
        "dominant_frequency_fft",
        "closest_reference_name",
        "mcmc_mean_A",
        "mcmc_mean_f",
        "mcmc_mean_phi",
        "mcmc_mean_sigma"
    }

    missing_keys = expected_keys - set(res.keys())
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

    assert res['closest_reference_name'] == 'Gamma_Burst', f"Incorrect reference matching: {res['closest_reference_name']} != Gamma_Burst"

    assert abs(res['dominant_frequency_fft'] - 3.14) < 0.05, f"FFT freq {res['dominant_frequency_fft']} out of bounds"
    assert abs(res['mcmc_mean_A'] - 2.5) < 0.1, f"MCMC A {res['mcmc_mean_A']} out of bounds"
    assert abs(res['mcmc_mean_f'] - 3.1415) < 0.05, f"MCMC f {res['mcmc_mean_f']} out of bounds"

    # Phase can be tricky due to wrapping, but based on the truth bounds, we'll use the provided check
    # phi_true = 1.0
    # The agent might find phi + 2pi, but the prior is [0, 2pi], so it should be near 1.0
    assert abs(res['mcmc_mean_phi'] - 1.0) < 0.2 or abs(res['mcmc_mean_phi'] - (1.0 + 2*3.1415926535)) < 0.2, f"MCMC phi {res['mcmc_mean_phi']} out of bounds"

    assert abs(res['mcmc_mean_sigma'] - 0.5) < 0.1, f"MCMC sigma {res['mcmc_mean_sigma']} out of bounds"