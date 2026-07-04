# test_final_state.py
import os
import json
import csv
import math
import pytest

def compute_true_sigma1():
    """Compute the largest singular value of the true data matrix using pure Python."""
    data_path = '/home/user/kinetics_data.csv'
    if not os.path.isfile(data_path):
        return 30.1585  # Fallback if file is missing, but test should fail elsewhere

    M = []
    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            M.append([float(row['A']), float(row['B']), float(row['C'])])

    # Compute M^T M (3x3 matrix)
    MTM = [[0.0]*3 for _ in range(3)]
    for row in M:
        for i in range(3):
            for j in range(3):
                MTM[i][j] += row[i] * row[j]

    # Power iteration to find the largest eigenvalue of M^T M
    v = [1.0, 1.0, 1.0]
    for _ in range(100):
        v_new = [sum(MTM[i][j] * v[j] for j in range(3)) for i in range(3)]
        norm = math.sqrt(sum(x*x for x in v_new))
        v = [x/norm for x in v_new]

    v_new = [sum(MTM[i][j] * v[j] for j in range(3)) for i in range(3)]
    eigenvalue = sum(v[i] * v_new[i] for i in range(3)) / sum(v[i] * v[i] for i in range(3))

    return math.sqrt(eigenvalue)

def test_best_fit_json_exists_and_valid():
    file_path = "/home/user/best_fit.json"
    assert os.path.isfile(file_path), f"Output file not found: {file_path}"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_keys = {"best_k1", "best_k2", "best_k3", "sse", "sigma_1"}
    assert expected_keys.issubset(data.keys()), f"JSON missing expected keys. Found: {list(data.keys())}"

def test_best_fit_values():
    file_path = "/home/user/best_fit.json"
    if not os.path.isfile(file_path):
        pytest.fail("Output file missing.")

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Check parameters
    assert abs(data.get("best_k1", -1) - 0.5) < 1e-4, f"Expected best_k1 to be 0.5000, got {data.get('best_k1')}"
    assert abs(data.get("best_k2", -1) - 0.2) < 1e-4, f"Expected best_k2 to be 0.2000, got {data.get('best_k2')}"
    assert abs(data.get("best_k3", -1) - 0.1) < 1e-4, f"Expected best_k3 to be 0.1000, got {data.get('best_k3')}"

    # Check SSE
    sse = data.get("sse", float('inf'))
    assert sse < 0.001, f"Expected SSE to be very close to 0, got {sse}"

    # Check sigma_1
    sigma_1_true = compute_true_sigma1()
    sigma_1 = data.get("sigma_1", -1)
    assert abs(sigma_1 - sigma_1_true) < 0.005, f"Expected sigma_1 to be near {sigma_1_true:.4f}, got {sigma_1}"