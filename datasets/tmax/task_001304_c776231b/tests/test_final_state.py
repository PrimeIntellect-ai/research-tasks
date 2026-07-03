# test_final_state.py
import os
import json

def test_clean_latency_csv():
    csv_path = '/home/user/clean_latency.csv'
    assert os.path.exists(csv_path), f"The file {csv_path} is missing."

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 500, f"Expected exactly 500 lines in {csv_path}, but found {len(lines)}."

    try:
        [float(x) for x in lines]
    except ValueError:
        assert False, f"Not all lines in {csv_path} are valid numerical values."

def test_fit_mcmc_script_exists():
    script_path = '/home/user/fit_mcmc.py'
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a valid file."

def test_profiling_results():
    json_path = '/home/user/profiling_results.json'
    assert os.path.exists(json_path), f"The file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {json_path} does not contain valid JSON."

    required_keys = {"mu1", "mu2", "wasserstein_distance", "n_samples"}
    missing_keys = required_keys - set(results.keys())
    assert not missing_keys, f"Missing required keys in {json_path}: {missing_keys}"

    assert results['n_samples'] == 500, f"Expected 'n_samples' to be 500, got {results['n_samples']}."

    assert isinstance(results['mu1'], (int, float)), "'mu1' must be a float."
    assert 17.0 <= results['mu1'] <= 23.0, f"'mu1' is out of the expected range (17.0 - 23.0): {results['mu1']}"

    assert isinstance(results['mu2'], (int, float)), "'mu2' must be a float."
    assert 74.0 <= results['mu2'] <= 86.0, f"'mu2' is out of the expected range (74.0 - 86.0): {results['mu2']}"

    assert isinstance(results['wasserstein_distance'], (int, float)), "'wasserstein_distance' must be a float."
    assert 0.0 <= results['wasserstein_distance'] <= 6.0, f"'wasserstein_distance' is out of expected bounds (0.0 - 6.0): {results['wasserstein_distance']}"