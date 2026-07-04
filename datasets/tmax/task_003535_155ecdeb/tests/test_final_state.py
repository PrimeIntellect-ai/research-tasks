# test_final_state.py

import os
import json
import subprocess
import sys
import math

def test_generate_spectra_uses_fsum():
    script_path = "/home/user/spectroscopy_ml/generate_spectra.py"
    assert os.path.isfile(script_path), f"Simulation script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "math.fsum" in content, (
        "The script generate_spectra.py does not appear to use math.fsum() "
        "as required for numerical stability."
    )

def test_bootstrap_script_exists():
    script_path = "/home/user/spectroscopy_ml/bootstrap_ci.py"
    assert os.path.isfile(script_path), f"Bootstrap script {script_path} is missing."

def test_results_json_exists_and_format():
    results_path = "/home/user/spectroscopy_ml/results.json"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file."

    expected_keys = {"stable_energy", "bootstrap_ci_lower", "bootstrap_ci_upper"}
    assert set(results.keys()) == expected_keys, (
        f"results.json must contain exactly the keys {expected_keys}. "
        f"Found: {set(results.keys())}"
    )

    assert isinstance(results["stable_energy"], float), "stable_energy must be a float."
    assert isinstance(results["bootstrap_ci_lower"], float), "bootstrap_ci_lower must be a float."
    assert isinstance(results["bootstrap_ci_upper"], float), "bootstrap_ci_upper must be a float."

def test_stable_energy_matches_script_output():
    script_path = "/home/user/spectroscopy_ml/generate_spectra.py"
    results_path = "/home/user/spectroscopy_ml/results.json"

    with open(results_path, "r") as f:
        results = json.load(f)

    # Run the student's script to get the true output
    proc = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )
    assert proc.returncode == 0, f"generate_spectra.py failed to run:\n{proc.stderr}"

    # Extract the total energy from the output
    output = proc.stdout
    energy_str = None
    for line in output.splitlines():
        if "Total Integrated Energy:" in line:
            energy_str = line.split(":")[-1].strip()
            break

    assert energy_str is not None, "Could not find 'Total Integrated Energy:' in script output."

    try:
        script_energy = float(energy_str)
    except ValueError:
        assert False, f"Could not parse energy value from script output: {energy_str}"

    assert math.isclose(results["stable_energy"], script_energy, rel_tol=1e-12), (
        f"stable_energy in results.json ({results['stable_energy']}) does not match "
        f"the output of generate_spectra.py ({script_energy})."
    )

def test_bootstrap_ci_values():
    results_path = "/home/user/spectroscopy_ml/results.json"
    with open(results_path, "r") as f:
        results = json.load(f)

    # Calculate expected CI using a subprocess to leverage numpy (since we can't import it directly)
    calc_script = """
import numpy as np
import csv

observations = []
with open('/home/user/spectroscopy_ml/observations.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        observations.append(float(row['intensity']))

np.random.seed(42)
n_iterations = 10000
bootstrapped_means = []
for _ in range(n_iterations):
    sample = np.random.choice(observations, size=len(observations), replace=True)
    bootstrapped_means.append(np.mean(sample))

lower = round(np.percentile(bootstrapped_means, 2.5), 3)
upper = round(np.percentile(bootstrapped_means, 97.5), 3)
print(f"{lower},{upper}")
"""
    proc = subprocess.run(
        [sys.executable, "-c", calc_script],
        capture_output=True,
        text=True
    )
    assert proc.returncode == 0, "Failed to compute expected bootstrap CI in test."

    expected_lower_str, expected_upper_str = proc.stdout.strip().split(",")
    expected_lower = float(expected_lower_str)
    expected_upper = float(expected_upper_str)

    assert math.isclose(results["bootstrap_ci_lower"], expected_lower, abs_tol=1e-3), (
        f"bootstrap_ci_lower is {results['bootstrap_ci_lower']}, expected {expected_lower}"
    )
    assert math.isclose(results["bootstrap_ci_upper"], expected_upper, abs_tol=1e-3), (
        f"bootstrap_ci_upper is {results['bootstrap_ci_upper']}, expected {expected_upper}"
    )