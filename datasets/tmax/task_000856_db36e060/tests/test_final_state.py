# test_final_state.py
import os
import json
import math
import subprocess
import pytest

PLOT_PATH = "/home/user/difference_plot.png"
JSON_PATH = "/home/user/analysis_results.json"

def get_golden_values():
    """
    Computes the expected values using a subprocess to leverage numpy and scipy
    already present in the environment, adhering to the standard-library-only rule
    for the pytest file itself while still dynamically computing the truth.
    """
    script = """
import numpy as np
import math
import os
import json
from scipy import stats

data_dir = "/home/user/sim_data"
energies_A = []
energies_B = []

for i in range(50):
    filename = os.path.join(data_dir, f"run_{i:02d}.npy")
    if not os.path.exists(filename):
        continue
    data = np.load(filename)

    v2 = np.sum(data**2, axis=1, dtype=np.float32)

    sum_A = np.sum(v2, dtype=np.float32)
    energies_A.append(float(sum_A))

    sum_B = math.fsum(v2.flatten())
    energies_B.append(sum_B)

diffs = np.array(energies_A) - np.array(energies_B)
mean_diff = np.mean(diffs)
max_abs_diff = np.max(np.abs(diffs))
t_stat, p_val = stats.ttest_rel(energies_A, energies_B)

golden_json = {
    "mean_difference": float(mean_diff),
    "max_abs_difference": float(max_abs_diff),
    "t_statistic": float(t_stat),
    "p_value": float(p_val)
}
print(json.dumps(golden_json))
"""
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Failed to compute golden values: {result.stderr}")
    return json.loads(result.stdout)

def test_difference_plot_exists_and_valid():
    assert os.path.exists(PLOT_PATH), f"Plot file not found at {PLOT_PATH}"
    assert os.path.isfile(PLOT_PATH), f"{PLOT_PATH} is not a file"

    with open(PLOT_PATH, "rb") as f:
        header = f.read(8)

    # Check for PNG magic number
    assert header == b"\x89PNG\r\n\x1a\n", f"{PLOT_PATH} is not a valid PNG image"

def test_analysis_results_json():
    assert os.path.exists(JSON_PATH), f"JSON results file not found at {JSON_PATH}"
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file"

    with open(JSON_PATH, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{JSON_PATH} does not contain valid JSON")

    expected_keys = {"mean_difference", "max_abs_difference", "t_statistic", "p_value"}
    actual_keys = set(results.keys())

    assert expected_keys.issubset(actual_keys), f"JSON is missing expected keys. Expected {expected_keys}, got {actual_keys}"

    golden = get_golden_values()

    for key in expected_keys:
        assert isinstance(results[key], (int, float)), f"Value for {key} must be a number"

        expected_val = golden[key]
        actual_val = results[key]

        # Use a relative tolerance of 1e-4 as specified
        assert math.isclose(actual_val, expected_val, rel_tol=1e-4, abs_tol=1e-7), \
            f"Value for {key} is incorrect. Expected approx {expected_val}, got {actual_val}"