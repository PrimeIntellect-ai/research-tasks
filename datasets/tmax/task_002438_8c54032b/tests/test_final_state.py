# test_final_state.py
import os
import json
import subprocess
import tempfile
import math
import pytest

def test_result_json_exists():
    assert os.path.exists("/home/user/result.json"), "/home/user/result.json does not exist."

def test_result_json_valid():
    with open("/home/user/result.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/result.json is not valid JSON.")

    assert "converged_N" in data, "Missing 'converged_N' in result.json."
    assert "ci_lower" in data, "Missing 'ci_lower' in result.json."
    assert "ci_upper" in data, "Missing 'ci_upper' in result.json."

def test_converged_N_and_confidence_intervals():
    with open("/home/user/result.json", "r") as f:
        data = json.load(f)

    # 1. Check converged_N
    assert data["converged_N"] == 20, f"Expected converged_N to be 20, got {data['converged_N']}."

    # 2. Recompute expected CI
    # Compile and run the generator to get the exact data
    with tempfile.TemporaryDirectory() as tmpdir:
        gen_src = "/home/user/generator.c"
        gen_bin = os.path.join(tmpdir, "generator")
        csv_out = os.path.join(tmpdir, "noisy_data.csv")

        # Modify the C file to output to our temp CSV to avoid side effects,
        # or just run it in a way that produces the file.
        # Actually, the C file hardcodes "/home/user/noisy_data.csv".
        # Let's just read the student's noisy_data.csv, but first verify it exists and was generated with N=20.
        student_csv = "/home/user/noisy_data.csv"
        assert os.path.exists(student_csv), f"{student_csv} does not exist."

        with open(student_csv, "r") as f:
            lines = f.read().strip().split("\n")

        assert len(lines) == 100, f"Expected 100 rows in {student_csv}, found {len(lines)}."

        parsed_data = []
        for line in lines:
            row = [float(x) for x in line.split(",")]
            assert len(row) == 21, f"Expected 21 columns (N=20) in {student_csv}, found {len(row)}."
            parsed_data.append(row)

        # Compute exact analytical solution for N=20
        N = 20
        exact_vals = []
        for i in range(N + 1):
            x = i / N
            val = math.sinh(1.0 - x) / math.sinh(1.0)
            exact_vals.append(val)

        # Compute MSEs
        mses = []
        for row in parsed_data:
            mse = sum((r - e) ** 2 for r, e in zip(row, exact_vals)) / len(exact_vals)
            mses.append(mse)

        # Bootstrap
        # We must use numpy to match the student's expected output
        try:
            import numpy as np
        except ImportError:
            pytest.fail("numpy is not installed, cannot verify bootstrap.")

        mses_np = np.array(mses)
        np.random.seed(42)

        bootstrapped_means = []
        for _ in range(10000):
            sample = np.random.choice(mses_np, size=100, replace=True)
            bootstrapped_means.append(np.mean(sample))

        expected_ci_lower = np.percentile(bootstrapped_means, 2.5)
        expected_ci_upper = np.percentile(bootstrapped_means, 97.5)

        # Check student's CI bounds
        student_ci_lower = data["ci_lower"]
        student_ci_upper = data["ci_upper"]

        assert abs(student_ci_lower - expected_ci_lower) < 1e-5, \
            f"ci_lower mismatch. Expected ~{expected_ci_lower:.6f}, got {student_ci_lower}"

        assert abs(student_ci_upper - expected_ci_upper) < 1e-5, \
            f"ci_upper mismatch. Expected ~{expected_ci_upper:.6f}, got {student_ci_upper}"