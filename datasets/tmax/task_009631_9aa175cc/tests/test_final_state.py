# test_final_state.py

import os
import pytest

def test_fast_sweep_script_exists_and_executable():
    script_path = "/home/user/fast_sweep.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable. Did you forget to chmod +x?"

def test_best_results_file_correctness():
    results_path = "/home/user/best_results.txt"
    samples_path = "/home/user/samples.txt"

    assert os.path.exists(results_path), f"The output file {results_path} does not exist."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    # Read samples and compute expected lowest costs
    assert os.path.exists(samples_path), f"The samples file {samples_path} is missing."

    samples = []
    with open(samples_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                x_str, y_str = line.split()
                samples.append((int(x_str), int(y_str)))

    # The cost function from simulate.sh is (x-42)^2 + (y-73)^2
    all_costs = sorted([(x - 42)**2 + (y - 73)**2 for x, y in samples])
    expected_top_3_costs = all_costs[:3]

    # Read actual results
    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {results_path}, found {len(lines)}."

    actual_costs = []
    for i, line in enumerate(lines):
        parts = line.split(',')
        assert len(parts) == 3, f"Line {i+1} in {results_path} does not match 'X,Y,cost' format: '{line}'"

        try:
            x, y, cost = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            pytest.fail(f"Line {i+1} in {results_path} contains non-integer values: '{line}'")

        expected_cost = (x - 42)**2 + (y - 73)**2
        assert cost == expected_cost, f"Reported cost {cost} for X={x}, Y={y} is incorrect. Expected {expected_cost}."
        assert (x, y) in samples, f"The point X={x}, Y={y} was not found in {samples_path}."

        actual_costs.append(cost)

    actual_costs.sort()
    assert actual_costs == expected_top_3_costs, (
        f"The extracted configurations do not have the lowest possible costs. "
        f"Expected costs: {expected_top_3_costs}, found: {actual_costs}"
    )