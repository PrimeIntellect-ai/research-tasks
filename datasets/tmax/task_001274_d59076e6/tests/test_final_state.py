# test_final_state.py

import os
import glob
import pytest

def compute_gd(X, Y, Z, alpha=0.01, iters=1000, lam=0.5):
    w1, w2, b = 0.0, 0.0, 0.0
    m = len(X)
    if m == 0:
        return 0.0, 0.0, 0.0
    for _ in range(iters):
        dw1, dw2, db = 0.0, 0.0, 0.0
        for i in range(m):
            pred = w1 * X[i] + w2 * Y[i] + b
            err = pred - Z[i]
            dw1 += err * X[i]
            dw2 += err * Y[i]
            db += err
        dw1 = dw1 / m + lam * w1
        dw2 = dw2 / m + lam * w2
        db = db / m
        w1 -= alpha * dw1
        w2 -= alpha * dw2
        b -= alpha * db
    return w1, w2, b

def parse_pdb(filepath):
    X, Y, Z = [], [], []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("ATOM  ") or line.startswith("HETATM"):
                try:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    X.append(x)
                    Y.append(y)
                    Z.append(z)
                except ValueError:
                    pass
    return X, Y, Z

def test_files_exist():
    assert os.path.isfile("/home/user/fit_plane.c"), "/home/user/fit_plane.c does not exist"
    assert os.path.isfile("/home/user/process_data.sh"), "/home/user/process_data.sh does not exist"
    assert os.access("/home/user/process_data.sh", os.X_OK), "/home/user/process_data.sh is not executable"
    assert os.path.isfile("/home/user/results.txt"), "/home/user/results.txt does not exist"

def test_results_content():
    pdb_dir = "/home/user/pdb_data/"
    pdb_files = sorted(glob.glob(os.path.join(pdb_dir, "*.pdb")))

    expected_lines = []
    for filepath in pdb_files:
        filename = os.path.basename(filepath)
        X, Y, Z = parse_pdb(filepath)
        w1, w2, b = compute_gd(X, Y, Z, alpha=0.01, iters=1000, lam=0.5)
        expected_lines.append(f"{filename}: w1: {w1:.4f}, w2: {w2:.4f}, b: {b:.4f}")

    with open("/home/user/results.txt", "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.txt, got {len(actual_lines)}"

    for expected, actual in zip(expected_lines, actual_lines):
        assert actual == expected, f"Expected line '{expected}', but got '{actual}'"