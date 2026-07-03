# test_final_state.py

import os
import json
import pytest

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"Expected output file {report_path} is missing."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    expected_keys = {"bootstrap_lower", "bootstrap_upper", "posterior_mean"}
    assert isinstance(report, dict), "The JSON output must be a dictionary."

    missing_keys = expected_keys - set(report.keys())
    assert not missing_keys, f"The JSON output is missing keys: {missing_keys}"

    for key in expected_keys:
        assert isinstance(report[key], (int, float)), f"Value for {key} must be a float."

def test_bayesian_posterior_mean():
    report_path = "/home/user/report.json"
    if not os.path.exists(report_path):
        pytest.skip("Report file missing.")

    with open(report_path, "r") as f:
        report = json.load(f)

    # The 'alpha' models that are deployed have run_ids 1 and 2.
    # Their errors are 5 and 3.
    # Prior: Gamma(alpha=2, beta=1)
    # Posterior shape = prior_alpha + sum(errors) = 2 + 5 + 3 = 10
    # Posterior rate = prior_beta + n = 1 + 2 = 3
    # Posterior mean = shape / rate = 10 / 3
    expected_posterior_mean = 10.0 / 3.0

    assert report.get("posterior_mean") == pytest.approx(expected_posterior_mean, rel=1e-5), \
        f"Expected posterior_mean to be {expected_posterior_mean}, but got {report.get('posterior_mean')}"

def test_bootstrap_bounds():
    report_path = "/home/user/report.json"
    if not os.path.exists(report_path):
        pytest.skip("Report file missing.")

    with open(report_path, "r") as f:
        report = json.load(f)

    lower = report.get("bootstrap_lower")
    upper = report.get("bootstrap_upper")

    # The 'beta' models that are deployed have errors: 2, 1, 4.
    # The minimum possible mean of a sample of size 3 is 1.0 (all 1s).
    # The maximum possible mean is 4.0 (all 4s).
    assert 1.0 <= lower <= 4.0, f"bootstrap_lower {lower} is out of theoretical bounds [1.0, 4.0]."
    assert 1.0 <= upper <= 4.0, f"bootstrap_upper {upper} is out of theoretical bounds [1.0, 4.0]."
    assert lower < upper, f"bootstrap_lower ({lower}) should be strictly less than bootstrap_upper ({upper})."

    # More tight bounds based on typical distribution of means from [1, 2, 4]
    assert 1.0 <= lower <= 2.0, f"bootstrap_lower {lower} seems incorrect for the data [1, 2, 4]."
    assert 2.6 <= upper <= 4.0, f"bootstrap_upper {upper} seems incorrect for the data [1, 2, 4]."