# test_final_state.py

import os
import json
import csv
import math
import pytest

def get_euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def compute_expected_densities():
    nodes_path = '/home/user/nodes.csv'
    defects_path = '/home/user/defects.csv'

    assert os.path.isfile(nodes_path), f"Missing {nodes_path}"
    assert os.path.isfile(defects_path), f"Missing {defects_path}"

    nodes = []
    with open(nodes_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes.append((float(row['x']), float(row['y'])))

    defects = []
    with open(defects_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            defects.append((float(row['x']), float(row['y'])))

    densities = []
    for dp in defects:
        # Find nodes within distance 5.0
        sub_nodes = [np for np in nodes if get_euclidean_distance(np, dp) < 5.0]
        v = len(sub_nodes)

        if v < 2:
            densities.append(0.0)
            continue

        # Count edges within distance 1.5
        edges = 0
        for i in range(v):
            for j in range(i + 1, v):
                if get_euclidean_distance(sub_nodes[i], sub_nodes[j]) < 1.5:
                    edges += 1

        density = (2.0 * edges) / (v * (v - 1))
        densities.append(density)

    return densities

def test_baseline_ci_json():
    json_path = '/home/user/baseline_ci.json'
    assert os.path.isfile(json_path), f"Output file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "lower_bound" in result, "Key 'lower_bound' missing in JSON output."
    assert "upper_bound" in result, "Key 'upper_bound' missing in JSON output."

    lower = result["lower_bound"]
    upper = result["upper_bound"]

    assert isinstance(lower, (int, float)), "'lower_bound' must be a number."
    assert isinstance(upper, (int, float)), "'upper_bound' must be a number."
    assert lower <= upper, "'lower_bound' should not be greater than 'upper_bound'."

    # Compute the expected densities using pure Python
    densities = compute_expected_densities()
    n = len(densities)
    assert n > 0, "No defects found to compute densities."

    mean_density = sum(densities) / n
    variance = sum((x - mean_density) ** 2 for x in densities) / n
    std_error = math.sqrt(variance / n)

    # 95% CI bounds approximated by Normal distribution (1.96 * SE)
    # The bootstrap CI should be very close to this analytical approximation
    approx_lower = mean_density - 1.96 * std_error
    approx_upper = mean_density + 1.96 * std_error

    # We allow a generous tolerance (e.g., 0.05) to account for bootstrap variation 
    # and differences in percentile methods or random seeds.
    assert math.isclose(lower, approx_lower, abs_tol=0.05), \
        f"lower_bound {lower} is too far from the expected approximate value {approx_lower:.4f}"

    assert math.isclose(upper, approx_upper, abs_tol=0.05), \
        f"upper_bound {upper} is too far from the expected approximate value {approx_upper:.4f}"

    # The true mean should definitely be contained within the student's CI
    assert lower <= mean_density <= upper, \
        f"The computed mean density ({mean_density:.4f}) is not within the reported CI [{lower}, {upper}]."