# test_final_state.py
import os
import pytest

def solve(c):
    x = 3.0
    for i in range(1, 101):
        fx = x**3 - 3*x - c
        if abs(fx) <= 1e-6:
            return x, i
        dfx = 3*x**2 - 3
        if dfx == 0:
            return x, 100
        x = x - fx / dfx
    return x, 100

def compute_expected_results(inputs_file):
    with open(inputs_file, 'r') as f:
        c_vals = [float(line.strip()) for line in f if line.strip()]

    unstable_count = 0
    iters_orig = []
    iters_pert = []

    for c in c_vals:
        r1, i1 = solve(c)
        r2, i2 = solve(c + 1e-4)

        iters_orig.append(i1)
        iters_pert.append(i2)

        if abs(r1 - r2) > 1e-2:
            unstable_count += 1

    def pmf(iters):
        counts = {}
        for i in iters:
            counts[i] = counts.get(i, 0) + 1
        total = len(iters)
        return {k: v/total for k, v in counts.items()}

    p_orig = pmf(iters_orig)
    p_pert = pmf(iters_pert)

    all_keys = set(p_orig.keys()).union(set(p_pert.keys()))
    tvd = 0.5 * sum(abs(p_orig.get(k, 0) - p_pert.get(k, 0)) for k in all_keys)

    max_iter_orig = max(iters_orig)

    return unstable_count, tvd, max_iter_orig

def test_profiling_report_exists():
    report_file = "/home/user/profiling_report.txt"
    assert os.path.isfile(report_file), f"Missing required output file: {report_file}"

def test_profiling_report_contents():
    inputs_file = "/home/user/inputs.txt"
    report_file = "/home/user/profiling_report.txt"

    assert os.path.isfile(inputs_file), f"Missing inputs file: {inputs_file}"
    assert os.path.isfile(report_file), f"Missing required output file: {report_file}"

    expected_unstable, expected_tvd, expected_max_iter = compute_expected_results(inputs_file)

    with open(report_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {report_file}, found {len(lines)}"

    actual_unstable = lines[0]
    actual_tvd = lines[1]
    actual_max_iter = lines[2]

    assert actual_unstable == str(expected_unstable), f"Line 1 (unstable count) mismatch: expected {expected_unstable}, got {actual_unstable}"

    expected_tvd_str = f"{expected_tvd:.4f}"
    assert actual_tvd == expected_tvd_str, f"Line 2 (TVD) mismatch: expected {expected_tvd_str}, got {actual_tvd}"

    assert actual_max_iter == str(expected_max_iter), f"Line 3 (max iterations) mismatch: expected {expected_max_iter}, got {actual_max_iter}"