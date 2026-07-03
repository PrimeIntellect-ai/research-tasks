# test_final_state.py

import os
import pytest

def test_solution_file_exists():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"File {solution_path} is missing. The C program must create this file."

def test_solution_content():
    network_path = "/home/user/network.txt"
    spectra_path = "/home/user/spectra.csv"
    solution_path = "/home/user/solution.txt"

    assert os.path.isfile(network_path), f"{network_path} is missing."
    assert os.path.isfile(spectra_path), f"{spectra_path} is missing."

    # 1. Compute the expected node (highest degree centrality)
    with open(network_path, "r") as f:
        lines = f.read().strip().split('\n')

    max_deg = -1
    best_node = -1
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        degree = sum(int(x) for x in line.strip().split())
        if degree > max_deg:
            max_deg = degree
            best_node = i

    # 2. Extract spectra for the best node
    x_vals = []
    y_vals = []
    with open(spectra_path, "r") as f:
        header = f.readline()
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            if int(parts[0]) == best_node:
                x_vals.append(float(parts[1]))
                y_vals.append(float(parts[2]))

    assert len(x_vals) > 0, f"No spectral data found for node {best_node}."

    # 3. Compute expected linear regression parameters (OLS)
    n = len(x_vals)
    sum_x = sum(x_vals)
    sum_y = sum(y_vals)
    sum_xx = sum(x * x for x in x_vals)
    sum_xy = sum(x * y for x, y in zip(x_vals, y_vals))

    det = n * sum_xx - sum_x**2
    b1 = (n * sum_xy - sum_x * sum_y) / det
    b0 = (sum_y - b1 * sum_x) / n

    expected_lines = [
        f"Node: {best_node}",
        f"Intercept: {b0:.4f}",
        f"Slope: {b1:.4f}"
    ]
    expected_content = "\n".join(expected_lines)

    # 4. Read and verify actual output
    with open(solution_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {solution_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{actual_content}"
    )