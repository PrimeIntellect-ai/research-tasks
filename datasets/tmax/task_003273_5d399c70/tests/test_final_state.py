# test_final_state.py

import os
import math
import pytest

def get_expected_t(p):
    t = 1.0
    for _ in range(100):
        f = 1.0 - math.exp(-0.5 * t) + 0.1 * t - p
        if abs(f) < 1e-6:
            break
        df = 0.5 * math.exp(-0.5 * t) + 0.1
        t = t - f / df
    return t

def test_divergence_times_csv():
    csv_path = "/home/user/divergence_times.csv"
    assert os.path.exists(csv_path), f"Missing file: {csv_path}"

    expected_p_values = [0.10, 0.25, 0.50, 0.75]

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_p_values), f"Expected {len(expected_p_values)} lines in {csv_path}, found {len(lines)}"

    for i, line in enumerate(lines):
        parts = line.split(',')
        assert len(parts) == 2, f"Invalid format in CSV line: {line}"

        p_val = float(parts[0])
        t_val = float(parts[1])

        expected_p = expected_p_values[i]
        expected_t = get_expected_t(expected_p)

        assert math.isclose(p_val, expected_p, abs_tol=1e-4), f"Expected p={expected_p}, got {p_val}"
        assert math.isclose(t_val, expected_t, abs_tol=1e-4), f"Expected t={expected_t:.4f} for p={p_val}, got {t_val}"

def test_plot_sh_exists():
    script_path = "/home/user/plot.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.path.isfile(script_path), f"Not a file: {script_path}"

def test_plot_txt():
    plot_path = "/home/user/plot.txt"
    assert os.path.exists(plot_path), f"Missing file: {plot_path}"

    expected_p_values = [0.10, 0.25, 0.50, 0.75]

    with open(plot_path, "r") as f:
        lines = [line.strip("\n") for line in f if line.strip("\n")]

    assert len(lines) == len(expected_p_values), f"Expected {len(expected_p_values)} lines in {plot_path}, found {len(lines)}"

    for i, line in enumerate(lines):
        expected_p = expected_p_values[i]
        expected_t = get_expected_t(expected_p)
        num_asterisks = int(math.floor(expected_t * 10))

        expected_p_str = f"{expected_p:.2f}"
        # The CSV might output 0.1 instead of 0.10, so we check if the line starts with the p value from the CSV
        # But the instructions say "exactly as it appears in the CSV".
        # Let's read the CSV to see exactly what was written.
        csv_path = "/home/user/divergence_times.csv"
        if os.path.exists(csv_path):
            with open(csv_path, "r") as csv_f:
                csv_lines = [l.strip() for l in csv_f if l.strip()]
                if i < len(csv_lines):
                    expected_p_str = csv_lines[i].split(',')[0]

        expected_line = f"{expected_p_str} | " + ("*" * num_asterisks)
        assert line == expected_line, f"Line {i+1} in {plot_path} is incorrect. Expected: '{expected_line}', Got: '{line}'"