# test_final_state.py

import os
import csv
import subprocess
import pytest

def euler_integration(k, y0, tEnd, dt=0.001):
    y = y0
    t = 0.0
    # To avoid floating point accumulation issues with the loop condition,
    # we can use a small epsilon or integer steps.
    # The Go code uses `for t < tEnd`
    while t < tEnd - 1e-9:
        y = y - dt * k * y
        t += dt
    return y

def test_ode_go_fixed():
    path = "/home/user/nanofit/ode.go"
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, "r") as f:
        content = f.read()
    assert "dt = dt * 1.5" not in content, "The bug 'dt = dt * 1.5' is still present in ode.go"

def test_go_test_passes():
    # Run go test to verify the test suite passes
    result = subprocess.run(
        ["go", "test"],
        cwd="/home/user/nanofit",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'go test' failed with output:\n{result.stdout}\n{result.stderr}"

def test_executable_exists():
    path = "/home/user/nanofit/nanofit"
    assert os.path.isfile(path), f"Compiled executable {path} is missing"
    assert os.access(path, os.X_OK), f"File {path} is not executable"

def test_results_csv_correct():
    path = "/home/user/results.csv"
    assert os.path.isfile(path), f"Results file {path} is missing"

    expected_results = {
        "seq1": euler_integration(5.0, 100.0, 2.0),
        "seq2": euler_integration(2.5, 50.0, 4.0),
        "seq3": euler_integration(10.0, 200.0, 1.0)
    }

    with open(path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "results.csv is empty"
    assert rows[0] == ["id", "final_signal"], "Header in results.csv is incorrect"

    parsed_results = {}
    for row in rows[1:]:
        assert len(row) == 2, f"Malformed row in results.csv: {row}"
        parsed_results[row[0]] = float(row[1])

    for seq_id, expected_val in expected_results.items():
        assert seq_id in parsed_results, f"{seq_id} missing from results.csv"
        actual_val = parsed_results[seq_id]
        # Check within a reasonable tolerance due to formatting (%.6f)
        assert abs(actual_val - expected_val) < 1e-4, f"Value for {seq_id} is incorrect. Expected approx {expected_val:.6f}, got {actual_val}"