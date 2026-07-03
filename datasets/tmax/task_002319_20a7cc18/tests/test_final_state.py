# test_final_state.py

import os
import json
import math
import pytest

def test_results_json_exists_and_valid():
    """Test that results.json exists, contains the correct keys, and correct values."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"File not found: {results_path}"

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected_keys = {"max_diff", "peak_index", "peak_magnitude"}
    assert set(results.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}"

    assert isinstance(results["peak_index"], int), "peak_index must be an integer"
    assert isinstance(results["max_diff"], float), "max_diff must be a float"
    assert isinstance(results["peak_magnitude"], float), "peak_magnitude must be a float"

    # Read the sequence to verify the values
    fasta_path = "/home/user/sequence.fasta"
    assert os.path.isfile(fasta_path), f"File not found: {fasta_path}"

    with open(fasta_path, "r") as f:
        lines = f.readlines()

    seq = "".join([l.strip() for l in lines if not l.startswith('>')])
    N = len(seq)
    assert N > 0, "Sequence is empty"

    # The expected peak index for the repeating pattern of length 11
    # is N / 11. For N=110,000, this is 10000.
    expected_peak_index = N // 11
    assert results["peak_index"] == expected_peak_index, \
        f"Expected peak_index to be {expected_peak_index}, got {results['peak_index']}"

    # Verify the peak magnitude by computing the DFT at the peak index in pure Python
    eiip = {'A': 0.1260, 'C': 0.1340, 'G': 0.0806, 'T': 0.1335}
    real = 0.0
    imag = 0.0
    peak_k = results["peak_index"]

    for n, char in enumerate(seq):
        val = eiip[char]
        angle = -2 * math.pi * peak_k * n / N
        real += val * math.cos(angle)
        imag += val * math.sin(angle)

    expected_mag = math.hypot(real, imag)

    assert math.isclose(results["peak_magnitude"], expected_mag, rel_tol=1e-3), \
        f"Expected peak_magnitude approx {expected_mag}, got {results['peak_magnitude']}"

    # max_diff should be greater than 0 due to float32 vs float64 precision differences
    assert results["max_diff"] > 0.0, "max_diff should be greater than 0.0"
    assert results["max_diff"] < 1.0, "max_diff is unexpectedly large"

def test_script_exists():
    """Test that the analysis script was created."""
    script_path = "/home/user/analyze_sequence.py"
    assert os.path.isfile(script_path), f"Script not found: {script_path}"