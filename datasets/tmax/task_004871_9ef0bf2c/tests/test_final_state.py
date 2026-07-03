# test_final_state.py
import os
import json
import math
import csv
import pytest
import numpy as np
import scipy.linalg

REPORT_FILE = "/home/user/stability_report.json"
DATA_FILE = "/home/user/data.csv"
SCRIPT_FILE = "/home/user/fit_model.py"

def deterministic_solve(N, data_file):
    dx = 1.0 / (N - 1)
    A = np.zeros((N, N))
    for i in range(N):
        A[i, i] = 2.0 / dx
        if i > 0: A[i, i-1] = -1.0 / dx
        if i < N-1: A[i, i+1] = -1.0 / dx
    A[0, 0] = 1.0 / dx; A[0, 1] = 0.0
    A[N-1, N-1] = 1.0 / dx; A[N-1, N-2] = 0.0

    b = np.zeros(N)
    with open(data_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            x_val, w = float(row[0]), float(row[1])
            idx = int(round(x_val * (N - 1)))
            # Deterministic accumulation (preserves order of file)
            b[idx] += w

    c, low = scipy.linalg.cho_factor(A)
    x = scipy.linalg.cho_solve((c, low), b)

    cond_A = np.linalg.cond(A)
    norm_x = np.linalg.norm(x)
    return cond_A, norm_x

def test_json_exists_and_structure():
    assert os.path.isfile(REPORT_FILE), f"Missing stability report file: {REPORT_FILE}"

    with open(REPORT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file stability_report.json is not valid JSON.")

    assert "N_10" in data, "Missing 'N_10' key in the JSON report."
    assert "N_20" in data, "Missing 'N_20' key in the JSON report."

    for key in ["N_10", "N_20"]:
        assert "cond_A" in data[key], f"Missing 'cond_A' under {key}."
        assert "norm_x" in data[key], f"Missing 'norm_x' under {key}."
        assert isinstance(data[key]["cond_A"], (int, float)), f"'cond_A' under {key} must be a number."
        assert isinstance(data[key]["norm_x"], (int, float)), f"'norm_x' under {key} must be a number."

def test_json_values():
    assert os.path.isfile(DATA_FILE), f"Missing data file: {DATA_FILE}"
    assert os.path.isfile(REPORT_FILE), f"Missing stability report file: {REPORT_FILE}"

    with open(REPORT_FILE, 'r') as f:
        data = json.load(f)

    expected_cond_10, expected_norm_10 = deterministic_solve(10, DATA_FILE)
    expected_cond_20, expected_norm_20 = deterministic_solve(20, DATA_FILE)

    # N_10 checks
    assert math.isclose(data["N_10"]["cond_A"], expected_cond_10, rel_tol=1e-5), \
        f"N_10 cond_A mismatch. Expected ~{expected_cond_10}, got {data['N_10']['cond_A']}"
    assert math.isclose(data["N_10"]["norm_x"], expected_norm_10, rel_tol=1e-5), \
        f"N_10 norm_x mismatch. Expected ~{expected_norm_10}, got {data['N_10']['norm_x']}"

    # N_20 checks
    assert math.isclose(data["N_20"]["cond_A"], expected_cond_20, rel_tol=1e-5), \
        f"N_20 cond_A mismatch. Expected ~{expected_cond_20}, got {data['N_20']['cond_A']}"
    assert math.isclose(data["N_20"]["norm_x"], expected_norm_20, rel_tol=1e-5), \
        f"N_20 norm_x mismatch. Expected ~{expected_norm_20}, got {data['N_20']['norm_x']}"

def test_cholesky_used_in_script():
    assert os.path.isfile(SCRIPT_FILE), f"Missing script file: {SCRIPT_FILE}"

    with open(SCRIPT_FILE, 'r') as f:
        content = f.read()

    assert "cho_factor" in content, "The script must use scipy.linalg.cho_factor."
    assert "cho_solve" in content, "The script must use scipy.linalg.cho_solve."
    assert "set(" not in content, "The script should not use sets for aggregation to ensure determinism."