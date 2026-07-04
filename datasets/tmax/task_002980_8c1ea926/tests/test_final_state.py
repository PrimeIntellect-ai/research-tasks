# test_final_state.py

import os
import json
import subprocess
import pytest

ANALYZE_SCRIPT = "/home/user/analyze.py"
RESULTS_JSON = "/home/user/results.json"

def test_analyze_script_exists():
    assert os.path.exists(ANALYZE_SCRIPT), f"The script {ANALYZE_SCRIPT} does not exist."
    assert os.path.isfile(ANALYZE_SCRIPT), f"The path {ANALYZE_SCRIPT} is not a file."

def test_results_json_exists_and_format():
    assert os.path.exists(RESULTS_JSON), f"The results file {RESULTS_JSON} does not exist."

    with open(RESULTS_JSON, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_JSON} is not valid JSON.")

    expected_keys = {"mu_mean", "hdi_3%", "hdi_97%"}
    assert set(data.keys()) == expected_keys, f"The JSON keys must be exactly {expected_keys}, found: {set(data.keys())}"

    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"The value for {key} must be a number."

def test_reproducibility_and_correctness():
    # Read the first run's results
    assert os.path.exists(RESULTS_JSON), f"The results file {RESULTS_JSON} does not exist."
    with open(RESULTS_JSON, 'r') as f:
        first_run_data = json.load(f)

    # Run the script again
    result = subprocess.run(["python3", ANALYZE_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {ANALYZE_SCRIPT} failed with error:\n{result.stderr}"

    # Read the second run's results
    with open(RESULTS_JSON, 'r') as f:
        second_run_data = json.load(f)

    # Check reproducibility
    assert first_run_data == second_run_data, (
        f"Results are not reproducible. "
        f"First run: {first_run_data}, Second run: {second_run_data}"
    )

    # Check statistical correctness
    mu_mean = second_run_data["mu_mean"]
    hdi_3 = second_run_data["hdi_3%"]
    hdi_97 = second_run_data["hdi_97%"]

    assert 54.0 <= mu_mean <= 56.0, f"mu_mean {mu_mean} is not between 54.0 and 56.0"
    assert 53.0 <= hdi_3 <= 55.0, f"hdi_3% {hdi_3} is not between 53.0 and 55.0"
    assert 55.0 <= hdi_97 <= 57.0, f"hdi_97% {hdi_97} is not between 55.0 and 57.0"