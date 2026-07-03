# test_final_state.py
import os
import json

def test_results_file_exists():
    results_path = '/home/user/results/fit_params.json'
    assert os.path.exists(results_path), f"Results file {results_path} is missing."
    assert os.path.isfile(results_path), f"Path {results_path} is not a file."

def test_results_json_content():
    results_path = '/home/user/results/fit_params.json'
    assert os.path.exists(results_path), "Cannot test content, results file is missing."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Could not parse JSON from {results_path}: {e}"

    assert 'f_0' in data, "Key 'f_0' is missing from the JSON output."
    assert 'sigma' in data, "Key 'sigma' is missing from the JSON output."

    f0 = data['f_0']
    sigma = data['sigma']

    assert isinstance(f0, (int, float)), f"f_0 must be a number, got {type(f0)}"
    assert isinstance(sigma, (int, float)), f"sigma must be a number, got {type(sigma)}"

    assert 2.4 < f0 < 2.6, f"f_0 value {f0} is out of expected bounds (2.4, 2.6)."
    assert 0.15 < sigma < 0.25, f"sigma value {sigma} is out of expected bounds (0.15, 0.25)."