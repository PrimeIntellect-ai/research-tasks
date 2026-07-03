# test_final_state.py
import os
import json
import math
import cmath
import pytest

def get_sequence():
    """Reads the sequence from the fasta file, ignoring the header."""
    file_path = "/home/user/sequence.fasta"
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r") as f:
        lines = f.readlines()
    seq = "".join(line.strip() for line in lines if not line.startswith(">"))
    return seq

def compute_expected_values(seq):
    """Computes the expected values using standard Python libraries."""
    eiip = {'A': 0.1260, 'C': 0.1340, 'G': 0.0806, 'T': 0.1335}

    # Map sequence
    try:
        signal = [eiip[base] for base in seq]
    except KeyError:
        return None

    N = len(signal)
    if N == 0 or N % 3 != 0:
        return None

    # Period 3 power: DFT at k = N / 3
    # X[k] = sum(x[n] * exp(-j * 2 * pi * k * n / N))
    # For k = N / 3, k/N = 1/3
    X_k = 0j
    for n, x in enumerate(signal):
        angle = -2 * math.pi * n / 3
        X_k += x * cmath.exp(1j * angle)
    p3_power = abs(X_k) ** 2

    # Analytical variance
    mean_val = sum(signal) / N
    variance = sum((x - mean_val) ** 2 for x in signal) / N
    analytical = N * variance

    return {
        "sequence_length": N,
        "period_3_power": round(p3_power, 4),
        "analytical_mean_power": round(analytical, 4)
    }

def test_run_analysis_script():
    """Check if run_analysis.sh exists and is executable."""
    script_path = "/home/user/run_analysis.sh"
    assert os.path.exists(script_path), f"Missing shell script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Shell script is not executable: {script_path}"

def test_notebook_exists():
    """Check if the Jupyter notebook exists."""
    notebook_path = "/home/user/period3_analysis.ipynb"
    assert os.path.exists(notebook_path), f"Missing Jupyter notebook: {notebook_path}"

def test_results_json():
    """Validate the contents of results.json."""
    json_path = "/home/user/results.json"
    assert os.path.exists(json_path), f"Missing results file: {json_path}"

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected_keys = {
        "sequence_length", 
        "period_3_power", 
        "bootstrap_95th_percentile", 
        "analytical_mean_power", 
        "is_coding"
    }
    assert set(results.keys()) == expected_keys, f"JSON keys do not match expected keys. Found: {list(results.keys())}"

    seq = get_sequence()
    expected = compute_expected_values(seq)
    assert expected is not None, "Could not compute expected values (invalid sequence)."

    assert results["sequence_length"] == expected["sequence_length"], \
        f"Expected sequence_length {expected['sequence_length']}, got {results['sequence_length']}"

    assert math.isclose(results["period_3_power"], expected["period_3_power"], abs_tol=0.0002), \
        f"Expected period_3_power ~{expected['period_3_power']}, got {results['period_3_power']}"

    assert math.isclose(results["analytical_mean_power"], expected["analytical_mean_power"], abs_tol=0.0002), \
        f"Expected analytical_mean_power ~{expected['analytical_mean_power']}, got {results['analytical_mean_power']}"

    # Bootstrap percentile is simulated via numpy, so we check against the known truth value for seed=42
    expected_bootstrap = 0.2831
    assert math.isclose(results["bootstrap_95th_percentile"], expected_bootstrap, abs_tol=0.005), \
        f"Expected bootstrap_95th_percentile ~{expected_bootstrap}, got {results['bootstrap_95th_percentile']}"

    expected_is_coding = results["period_3_power"] > results["bootstrap_95th_percentile"]
    assert results["is_coding"] == expected_is_coding, \
        f"Expected is_coding to be {expected_is_coding}, got {results['is_coding']}"