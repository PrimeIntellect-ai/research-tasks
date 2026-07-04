# test_final_state.py
import os
import pytest

def test_c_source_file_exists():
    source_path = "/home/user/mcmc_profiler.c"
    assert os.path.exists(source_path), f"Source file {source_path} is missing."
    assert os.path.isfile(source_path), f"{source_path} is not a file."

def test_results_file_exists_and_format():
    results_path = "/home/user/profiler_results.txt"
    assert os.path.exists(results_path), f"Results file {results_path} is missing."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    expected_keys = {"w", "mu1", "mu2", "kl_divergence"}
    parsed_keys = set()

    with open(results_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            assert ":" in line, f"Invalid format in results file. Line missing colon: '{line}'"
            key, val_str = line.split(":", 1)
            key = key.strip()
            val_str = val_str.strip()

            assert key in expected_keys, f"Unexpected key '{key}' found in results file."
            try:
                float(val_str)
            except ValueError:
                pytest.fail(f"Value for '{key}' is not a valid float: '{val_str}'")
            parsed_keys.add(key)

    missing_keys = expected_keys - parsed_keys
    assert not missing_keys, f"Missing expected keys in results file: {missing_keys}"

def test_results_values_within_bounds():
    results_path = "/home/user/profiler_results.txt"
    if not os.path.exists(results_path):
        pytest.skip("Results file missing, skipping bounds check.")

    res = {}
    with open(results_path, "r") as f:
        for line in f:
            if ":" in line:
                key, val = line.split(":", 1)
                res[key.strip()] = float(val.strip())

    if "w" in res:
        assert 0.28 <= res["w"] <= 0.42, f"w out of bounds: {res['w']}. Expected between 0.28 and 0.42."
    if "mu1" in res:
        assert 3.7 <= res["mu1"] <= 4.3, f"mu1 out of bounds: {res['mu1']}. Expected between 3.7 and 4.3."
    if "mu2" in res:
        assert 10.7 <= res["mu2"] <= 11.3, f"mu2 out of bounds: {res['mu2']}. Expected between 10.7 and 11.3."
    if "kl_divergence" in res:
        assert res["kl_divergence"] < 0.1, f"KL divergence too high: {res['kl_divergence']}. Expected < 0.1."