# test_final_state.py
import os
import csv
import math
import random
import pytest

def lcg_runif(s, min_val, max_val):
    s = (1103515245 * s + 12345) % 2147483648
    v = min_val + (max_val - min_val) * (s / 2147483648.0)
    return s, v

def simulate_cpp(k, x_min, x_max, y_min, y_max, samples, seed):
    current_seed = seed
    total_val = 0.0
    for _ in range(samples):
        current_seed, x = lcg_runif(current_seed, x_min, x_max)
        current_seed, y = lcg_runif(current_seed, y_min, y_max)
        val = max(0.0, math.sin(k * x) * math.cos(k * y))
        total_val += val
    area = (x_max - x_min) * (y_max - y_min)
    return (total_val / samples) * area

def get_expected_results():
    results = {}
    for N in [2, 4, 8]:
        random.seed(42)
        k_vals = [random.uniform(1.0, 5.0) for _ in range(50)]

        best_k = None
        max_integral = -1.0

        for k in k_vals:
            total_integral = 0.0
            for i in range(N):
                for j in range(N):
                    x_min = i * math.pi / N
                    x_max = (i + 1) * math.pi / N
                    y_min = j * math.pi / N
                    y_max = (j + 1) * math.pi / N

                    integral = simulate_cpp(k, x_min, x_max, y_min, y_max, 1000, 42)
                    total_integral += integral

            if total_integral > max_integral:
                max_integral = total_integral
                best_k = k

        results[str(N)] = (round(best_k, 4), round(max_integral, 4))
    return results

def test_csv_results():
    csv_path = "/home/user/stability_results.csv"
    assert os.path.exists(csv_path), f"The output file {csv_path} is missing. The script did not generate the required output."

    expected = get_expected_results()

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["N", "best_k", "max_integral"], f"CSV header is incorrect. Expected ['N', 'best_k', 'max_integral'], got {header}."

        rows = list(reader)
        assert len(rows) == 3, f"CSV should contain exactly 3 data rows, got {len(rows)}."

        for row in rows:
            assert len(row) == 3, f"Each row must have exactly 3 columns, got {len(row)} in row: {row}."
            n_str, k_str, int_str = row

            assert n_str in expected, f"Unexpected N value in CSV: {n_str}"

            try:
                k_val = float(k_str)
                int_val = float(int_str)
            except ValueError:
                pytest.fail(f"Could not parse numerical values in row: {row}")

            expected_k, expected_int = expected[n_str]

            assert abs(k_val - expected_k) <= 0.0002, \
                f"For N={n_str}, expected best_k ~ {expected_k}, got {k_val}."
            assert abs(int_val - expected_int) <= 0.0002, \
                f"For N={n_str}, expected max_integral ~ {expected_int}, got {int_val}."