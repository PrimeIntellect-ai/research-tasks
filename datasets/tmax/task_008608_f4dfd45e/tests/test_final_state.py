# test_final_state.py

import os
import re
import math
import pytest

def test_executable_exists():
    executable_path = "/home/user/simulate_decay"
    assert os.path.exists(executable_path), f"The executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_data_csv_exists_and_format():
    data_path = "/home/user/data.csv"
    assert os.path.exists(data_path), f"The data file {data_path} is missing."

    with open(data_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 101, f"Expected 101 lines in data.csv (header + 100 data points), but found {len(lines)}."
    assert lines[0].strip() == "t,y", "The header of data.csv should be 't,y'."

    # Check that data points are valid numbers
    for i, line in enumerate(lines[1:], start=1):
        parts = line.split(",")
        assert len(parts) == 2, f"Line {i+1} does not have exactly two columns: {line}"
        try:
            float(parts[0])
            float(parts[1])
        except ValueError:
            pytest.fail(f"Line {i+1} contains non-numeric data: {line}")

def test_stats_result():
    result_path = "/home/user/stats_result.txt"
    assert os.path.exists(result_path), f"The results file {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    lines = content.split("\n")
    assert len(lines) == 4, f"Expected exactly 4 lines in stats_result.txt, found {len(lines)}."

    patterns = [
        r"^Model 0 RSS:\s*([0-9.]+)$",
        r"^Model 1 RSS:\s*([0-9.]+)$",
        r"^F-statistic:\s*([0-9.]+)$",
        r"^p-value:\s*([0-9.]+)$"
    ]

    values = []
    for i, (line, pattern) in enumerate(zip(lines, patterns)):
        match = re.match(pattern, line.strip())
        assert match, f"Line {i+1} does not match the required format. Got: '{line}'"
        values.append(float(match.group(1)))

    rss0, rss1, f_stat, p_val = values

    # Check that RSS values are reasonable for the given problem
    # RSS1 should be around 1.0 (variance ~0.01 * 100 points)
    # RSS0 should be significantly higher (around 15-20)
    assert 0.5 < rss1 < 3.0, f"Model 1 RSS ({rss1}) is outside the expected range for a good fit."
    assert 10.0 < rss0 < 40.0, f"Model 0 RSS ({rss0}) is outside the expected range."
    assert rss1 < rss0, "Model 1 RSS should be lower than Model 0 RSS."

    # Recompute F-statistic
    # Model 0 df = N - 2 = 98
    # Model 1 df = N - 4 = 96
    # F = ((RSS0 - RSS1) / (4 - 2)) / (RSS1 / (100 - 4))
    expected_f_stat = ((rss0 - rss1) / 2.0) / (rss1 / 96.0)

    # Allow a small tolerance for rounding differences
    f_stat_diff = abs(f_stat - expected_f_stat)
    assert f_stat_diff / expected_f_stat < 0.05, \
        f"Reported F-statistic {f_stat} does not match the expected value {expected_f_stat:.4f} computed from the reported RSS values."

    # Check p-value
    assert 0.0 <= p_val < 0.01, f"Expected a very small p-value, but got {p_val}."