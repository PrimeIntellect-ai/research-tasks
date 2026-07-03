# test_final_state.py

import os
import math
import pytest

def get_expected_results():
    def simulate(N):
        state = 42
        def my_drand():
            nonlocal state
            state = (state * 1103515245 + 12345) % 2147483648
            return state / 2147483648.0

        counts = [0] * 5
        pos = 0
        for _ in range(N):
            r = my_drand()
            if r < 0.7:
                pos = (pos + 1) % 5
            counts[pos] += 1

        freqs = [c / N for c in counts]
        l2_error = math.sqrt(sum((f - 0.2)**2 for f in freqs))
        return freqs, l2_error

    results = {}
    for N in [1000, 10000, 100000, 1000000]:
        results[N] = simulate(N)
    return results

def test_simulate_c_exists():
    file_path = "/home/user/simulate.c"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_convergence_log():
    log_path = "/home/user/convergence_log.csv"
    assert os.path.exists(log_path), f"The file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines (1 header + 4 data rows) in {log_path}, got {len(lines)}."
    assert lines[0] == "N,L2_error", f"Incorrect header in {log_path}. Expected 'N,L2_error', got '{lines[0]}'."

    expected_results = get_expected_results()

    parsed_Ns = set()
    for line in lines[1:]:
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid line format in {log_path}: '{line}'. Expected 'N,L2_error'."
        try:
            N = int(parts[0])
            l2_error = float(parts[1])
        except ValueError:
            pytest.fail(f"Could not parse integers/floats from line: '{line}'.")

        assert N in expected_results, f"Unexpected N value in {log_path}: {N}. Expected one of {list(expected_results.keys())}."
        parsed_Ns.add(N)

        expected_l2 = expected_results[N][1]
        assert math.isclose(l2_error, expected_l2, abs_tol=1e-5), \
            f"For N={N}, expected L2 error approximately {expected_l2:.6f}, got {l2_error}."

    assert parsed_Ns == set(expected_results.keys()), f"Missing N values in {log_path}. Expected {set(expected_results.keys())}, got {parsed_Ns}."

def test_max_diff():
    diff_path = "/home/user/max_diff.txt"
    assert os.path.exists(diff_path), f"The file {diff_path} is missing."

    with open(diff_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse float from {diff_path}. Content: '{content}'.")

    expected_results = get_expected_results()
    freqs = expected_results[1000000][0]
    ref = [0.201, 0.198, 0.205, 0.196, 0.200]

    max_diff = max(abs(f - r) for f, r in zip(freqs, ref))

    assert math.isclose(val, max_diff, abs_tol=1e-5), \
        f"Incorrect max difference in {diff_path}. Expected approximately {max_diff:.6f}, got {val}."