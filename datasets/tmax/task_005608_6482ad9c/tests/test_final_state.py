# test_final_state.py
import os
import json

def test_script_exists():
    script_path = "/home/user/analyze_spectra.py"
    assert os.path.isfile(script_path), f"Missing required script: {script_path}"

def test_results_json_exists_and_format():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Missing required file: {results_path}"

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not valid JSON."

    expected_keys = {"k_estimate", "ci_lower", "ci_upper"}
    assert set(results.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, found {set(results.keys())}"

    for key in expected_keys:
        assert isinstance(results[key], (int, float)), f"Value for {key} must be a number."

def test_results_values():
    results_path = "/home/user/results.json"
    if not os.path.isfile(results_path):
        return  # Handled by previous test

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            return  # Handled by previous test

    if not set(results.keys()) == {"k_estimate", "ci_lower", "ci_upper"}:
        return

    k_est = results["k_estimate"]
    ci_lower = results["ci_lower"]
    ci_upper = results["ci_upper"]

    # Check ordering of CI
    assert ci_lower <= k_est <= ci_upper, f"Confidence interval [{ci_lower}, {ci_upper}] does not contain the estimate {k_est}."

    # Verify against expected truth values with tolerance
    assert abs(k_est - 2.5539) < 0.05, f"k_estimate {k_est} is out of expected range (expected ~2.5539)."
    assert abs(ci_lower - 2.4544) < 0.05, f"ci_lower {ci_lower} is out of expected range (expected ~2.4544)."
    assert abs(ci_upper - 2.6582) < 0.05, f"ci_upper {ci_upper} is out of expected range (expected ~2.6582)."