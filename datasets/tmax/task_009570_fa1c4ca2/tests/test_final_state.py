# test_final_state.py

import os
import glob
import math

def compute_expected_features():
    results = []
    graph_files = glob.glob("/home/user/graphs/graph_*.txt")
    for file_path in graph_files:
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        with open(file_path, 'r') as f:
            weights = [float(line.strip().split()[2]) for line in f if line.strip()]

        # Sort strictly ascending
        weights.sort()

        # Sequential summation to match awk
        total = 0.0
        for w in weights:
            total += w

        results.append((name, total))

    # Sort alphabetically by filename
    results.sort(key=lambda x: x[0])
    return results

def test_calc_energy_script_exists():
    """Check if the bash script exists and is executable."""
    script_path = "/home/user/calc_energy.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_features_file_correctness():
    """Check if features.txt is created and contains the correct formatted sums."""
    features_path = "/home/user/features.txt"
    assert os.path.isfile(features_path), f"Output file {features_path} is missing."

    expected_results = compute_expected_features()

    with open(features_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_results), f"Expected {len(expected_results)} lines in {features_path}, found {len(lines)}."

    for i, (expected_name, expected_total) in enumerate(expected_results):
        expected_line = f"{expected_name}: {expected_total:.10f}"
        assert lines[i] == expected_line, f"Mismatch at line {i+1}. Expected '{expected_line}', got '{lines[i]}'."

def test_validation_file_correctness():
    """Check if validation.txt contains the correct absolute difference."""
    validation_path = "/home/user/validation.txt"
    assert os.path.isfile(validation_path), f"Validation file {validation_path} is missing."

    with open(validation_path, 'r') as f:
        content = f.read().strip()

    try:
        diff_value = float(content)
    except ValueError:
        pytest.fail(f"Content of {validation_path} is not a valid float: '{content}'")

    assert diff_value >= 0, f"Absolute difference cannot be negative, got {diff_value}."
    assert diff_value <= 1e-10, f"Absolute difference {diff_value} is too large. Expected <= 1e-10."