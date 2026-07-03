# test_final_state.py

import json
import os
import subprocess
import pytest

RESULTS_PATH = '/app/tinyexpr-py/results.json'
TEST_FILE_PATH = '/app/tinyexpr-py/test_te.py'

def test_results_json_exists():
    assert os.path.isfile(RESULTS_PATH), f"{RESULTS_PATH} was not generated. Did you run benchmark.py?"

def test_metrics_thresholds():
    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {RESULTS_PATH} as valid JSON.")

    assert 'mse' in data, f"{RESULTS_PATH} is missing the 'mse' key."
    assert 'speedup' in data, f"{RESULTS_PATH} is missing the 'speedup' key."

    mse = data['mse']
    speedup = data['speedup']

    # Thresholds defined by the truth data
    expected_mse_threshold = 1e-7
    expected_speedup_threshold = 10.0

    assert mse < expected_mse_threshold, f"MSE too high: {mse} (expected < {expected_mse_threshold})"
    assert speedup >= expected_speedup_threshold, f"Speedup too low: {speedup}x (expected >= {expected_speedup_threshold}x)"

def test_test_te_passes():
    assert os.path.isfile(TEST_FILE_PATH), f"{TEST_FILE_PATH} is missing."

    # Run pytest on the test file to ensure the fixtures and tests are fixed
    result = subprocess.run(
        ['pytest', TEST_FILE_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"pytest {TEST_FILE_PATH} failed to pass. Output:\n{result.stdout}\n{result.stderr}"