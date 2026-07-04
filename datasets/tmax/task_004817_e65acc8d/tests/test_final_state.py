# test_final_state.py

import os
import json
import subprocess
import sys

def test_executable_exists():
    executable_path = "/home/user/sim/sim"
    assert os.path.isfile(executable_path), f"The compiled executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_output_files_exist():
    coarse_path = "/home/user/coarse.txt"
    fine_path = "/home/user/fine.txt"

    assert os.path.isfile(coarse_path), f"The file {coarse_path} does not exist."
    assert os.path.isfile(fine_path), f"The file {fine_path} does not exist."

    with open(coarse_path, "r") as f:
        coarse_lines = f.read().splitlines()
    assert len(coarse_lines) == 1000, f"Expected 1000 lines in {coarse_path}, found {len(coarse_lines)}."

    with open(fine_path, "r") as f:
        fine_lines = f.read().splitlines()
    assert len(fine_lines) == 2000, f"Expected 2000 lines in {fine_path}, found {len(fine_lines)}."

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"The file {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {results_path} does not contain valid JSON."

    expected_keys = {"distance", "ci_lower", "ci_upper"}
    assert set(actual.keys()) == expected_keys, f"Expected keys {expected_keys} in {results_path}, found {set(actual.keys())}."

    # Compute expected values using a subprocess to access numpy and scipy installed in the environment
    script = """
import numpy as np
from scipy.stats import wasserstein_distance
import json

coarse = np.loadtxt("/home/user/coarse.txt")
fine = np.loadtxt("/home/user/fine.txt")

dist = wasserstein_distance(coarse, fine)

np.random.seed(42)
boot_dists = []
for _ in range(1000):
    c_boot = np.random.choice(coarse, size=len(coarse), replace=True)
    f_boot = np.random.choice(fine, size=len(fine), replace=True)
    boot_dists.append(wasserstein_distance(c_boot, f_boot))

ci_lower = np.percentile(boot_dists, 2.5)
ci_upper = np.percentile(boot_dists, 97.5)

print(json.dumps({
    "distance": round(dist, 4),
    "ci_lower": round(ci_lower, 4),
    "ci_upper": round(ci_upper, 4)
}))
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compute expected values. Ensure numpy and scipy are installed. Error: {result.stderr}"

    expected = json.loads(result.stdout)

    for key in expected_keys:
        assert isinstance(actual[key], (int, float)), f"Value for {key} must be a number."
        diff = abs(actual[key] - expected[key])
        assert diff <= 1e-4, f"Value for {key} is incorrect. Expected {expected[key]}, got {actual[key]}."