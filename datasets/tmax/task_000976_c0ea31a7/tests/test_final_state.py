# test_final_state.py
import os
import json
import math
import glob

def get_matrix_from_csv(filepath):
    matrix = []
    with open(filepath, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            row = [float(x) for x in line.strip().split(',')]
            matrix.append(row)
    return matrix

def compute_covariance(matrix):
    n = len(matrix)
    m = len(matrix[0])
    means = [sum(matrix[i][j] for i in range(n)) / n for j in range(m)]

    cov = [[0.0 for _ in range(m)] for _ in range(m)]
    for j in range(m):
        for k in range(m):
            s = sum((matrix[i][j] - means[j]) * (matrix[i][k] - means[k]) for i in range(n))
            cov[j][k] = s / (n - 1)
    return cov

def compute_determinant_3x3(mat):
    a, b, c = mat[0]
    d, e, f = mat[1]
    g, h, i = mat[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

def test_cpp_file_exists():
    cpp_files = glob.glob("/home/user/*.cpp")
    assert len(cpp_files) > 0, "No C++ (.cpp) file found in /home/user/"

def test_tracker_json_exists():
    assert os.path.isfile("/home/user/tracker.json"), "/home/user/tracker.json does not exist."

def test_tracker_json_contents():
    tracker_path = "/home/user/tracker.json"
    with open(tracker_path, 'r') as f:
        try:
            tracker = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/tracker.json is not valid JSON."

    expected_results = {}
    for name in ["exp_alpha", "exp_beta", "exp_gamma"]:
        csv_path = f"/home/user/experiments/{name}.csv"
        matrix = get_matrix_from_csv(csv_path)
        cov = compute_covariance(matrix)
        # Regularize
        for i in range(3):
            cov[i][i] += 0.1

        det = compute_determinant_3x3(cov)
        expected_results[name] = round(det, 4)

    best_exp = min(["exp_alpha", "exp_beta", "exp_gamma"], key=lambda k: expected_results[k])

    for name in ["exp_alpha", "exp_beta", "exp_gamma"]:
        assert name in tracker, f"Missing key '{name}' in tracker.json"
        assert isinstance(tracker[name], (int, float)), f"Value for '{name}' must be a number."
        assert math.isclose(tracker[name], expected_results[name], abs_tol=0.0002), \
            f"Value for '{name}' is {tracker[name]}, expected {expected_results[name]} (±0.0001)."

    assert "best" in tracker, "Missing key 'best' in tracker.json"
    assert tracker["best"] == best_exp, f"Expected 'best' to be '{best_exp}', got '{tracker['best']}'."