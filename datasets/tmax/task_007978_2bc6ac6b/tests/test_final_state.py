# test_final_state.py

import os
import pytest
import math

def compute_expected_results():
    raw_signal_path = "/home/user/raw_signal.tsv"
    assert os.path.exists(raw_signal_path), f"Input file {raw_signal_path} is missing."

    with open(raw_signal_path, "r") as f:
        S = [float(line.strip()) for line in f if line.strip()]

    N = len(S)
    iterations = 0

    while True:
        iterations += 1
        S_new = [0.0] * N
        S_new[0] = S[0]
        S_new[N-1] = S[N-1]

        max_change = 0.0
        for i in range(1, N-1):
            S_new[i] = 0.5 * S[i] + 0.25 * S[i-1] + 0.25 * S[i+1]
            change = abs(S_new[i] - S[i])
            if change > max_change:
                max_change = change

        S = S_new
        if max_change < 0.001:
            break

    energy = sum(x**2 for x in S)

    return iterations, energy, S

def test_script_exists_and_executable():
    """Check if the bash script exists and is executable."""
    script_path = "/home/user/analyze_squiggles.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_iterations_output():
    """Check if iterations.txt contains the correct number of iterations."""
    output_path = "/home/user/iterations.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    expected_iterations, _, _ = compute_expected_results()

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == str(expected_iterations), f"Expected {expected_iterations} iterations, but got {content} in {output_path}."

def test_final_energy_output():
    """Check if final_energy.txt contains the correct energy value."""
    output_path = "/home/user/final_energy.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    _, expected_energy, _ = compute_expected_results()
    expected_energy_str = f"{expected_energy:.4f}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == expected_energy_str, f"Expected energy {expected_energy_str}, but got {content} in {output_path}."

def test_smoothed_signal_output():
    """Check if smoothed.tsv contains the correctly smoothed signal."""
    output_path = "/home/user/smoothed.tsv"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    _, _, expected_signal = compute_expected_results()

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_signal), f"Expected {len(expected_signal)} lines in {output_path}, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_signal)):
        expected_str = f"{expected:.6f}"
        # Parse actual to float to allow minor formatting differences, but compare up to 6 decimals
        try:
            actual_float = float(actual)
        except ValueError:
            pytest.fail(f"Line {i+1} in {output_path} is not a valid float: '{actual}'")

        assert math.isclose(actual_float, float(expected_str), abs_tol=1e-5), \
            f"Line {i+1} mismatch: expected {expected_str}, got {actual}."