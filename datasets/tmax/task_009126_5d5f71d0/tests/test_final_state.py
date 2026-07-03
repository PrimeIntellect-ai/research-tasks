# test_final_state.py

import os
import math
import pytest

def get_expected_probs():
    expected = {}
    for i in range(1, 5):
        trace_file = f"/home/user/traces/trace_{i}.txt"
        if not os.path.isfile(trace_file):
            continue

        with open(trace_file, "r") as f:
            data = [float(line.strip()) for line in f.readlines()]

        n = len(data)
        h = 0.5
        sqrt_2pi = 2.506628
        start = 2.0
        end = 5.0
        steps = 100

        dx = (end - start) / steps
        total_area = 0.0

        for j in range(steps):
            x = start + j * dx

            kde_sum = 0.0
            for xi in data:
                u = (x - xi) / h
                k_u = (1.0 / sqrt_2pi) * math.exp(- (u**2) / 2.0)
                kde_sum += k_u

            f_hat = (1.0 / (n * h)) * kde_sum
            total_area += f_hat * dx

        expected[f"trace_{i}.txt"] = total_area
    return expected

def test_scripts_exist_and_executable():
    """Ensure the required scripts exist and are executable."""
    scripts = [
        "/home/user/kde.sh",
        "/home/user/prob.sh",
        "/home/user/analyze.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Required script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_results_file():
    """Ensure the results file exists and has the correct format and values."""
    results_file = "/home/user/results/probs.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

    with open(results_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {results_file}, found {len(lines)}."

    expected_probs = get_expected_probs()
    assert len(expected_probs) == 4, "Trace files missing, unable to compute expected probabilities."

    parsed_results = {}
    for line in lines:
        parts = line.split(":")
        assert len(parts) == 2, f"Invalid format in line: '{line}'. Expected 'trace_N.txt: <value>'."
        filename = parts[0].strip()
        try:
            val = float(parts[1].strip())
        except ValueError:
            pytest.fail(f"Invalid probability value in line: '{line}'.")
        parsed_results[filename] = val

    # Check alphabetical sorting
    filenames = list(parsed_results.keys())
    assert filenames == sorted(filenames), "Results are not sorted alphabetically by filename."

    for filename, expected_val in expected_probs.items():
        assert filename in parsed_results, f"Missing result for {filename}."
        actual_val = parsed_results[filename]
        assert abs(actual_val - expected_val) <= 0.0002, (
            f"Value for {filename} is incorrect. "
            f"Expected approx {expected_val:.4f}, got {actual_val:.4f}."
        )