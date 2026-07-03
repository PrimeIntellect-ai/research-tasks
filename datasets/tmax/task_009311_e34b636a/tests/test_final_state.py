# test_final_state.py

import os
import csv
import math
import pytest

def compute_expected_data():
    raw_path = "/home/user/raw_data.csv"
    assert os.path.exists(raw_path), f"Missing {raw_path}"

    filtered_rows = []
    y_values = []

    with open(raw_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row:
                continue
            id_val = int(row[0])
            f1 = float(row[1])
            f2 = float(row[2])
            f3 = float(row[3])

            y = 2.0 + 0.5 * f1 - 1.2 * f2 + 0.8 * f3

            if y > 0.0:
                filtered_rows.append([str(id_val), f"{f1:.4f}", f"{f2:.4f}", f"{f3:.4f}", f"{y:.4f}"])
                y_values.append(y)

    n = len(y_values)
    mean_y = sum(y_values) / n
    var_y = sum((y - mean_y) ** 2 for y in y_values) / (n - 1)
    se_y = math.sqrt(var_y) / math.sqrt(n)

    lower = mean_y - 1.96 * se_y
    upper = mean_y + 1.96 * se_y

    stats = {
        "Mean": f"{mean_y:.4f}",
        "CI_Lower": f"{lower:.4f}",
        "CI_Upper": f"{upper:.4f}"
    }

    return filtered_rows, stats

def test_filtered_data_csv():
    expected_rows, _ = compute_expected_data()
    out_path = "/home/user/filtered_data.csv"

    assert os.path.exists(out_path), f"Missing {out_path}"

    with open(out_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id", "f1", "f2", "f3", "y"], "Incorrect header in filtered_data.csv"

        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, found {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}"

def test_stats_txt():
    _, expected_stats = compute_expected_data()
    out_path = "/home/user/stats.txt"

    assert os.path.exists(out_path), f"Missing {out_path}"

    actual_stats = {}
    with open(out_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                actual_stats[k.strip()] = v.strip()

    for key in ["Mean", "CI_Lower", "CI_Upper"]:
        assert key in actual_stats, f"Missing {key} in stats.txt"
        assert actual_stats[key] == expected_stats[key], f"Expected {key} to be {expected_stats[key]}, got {actual_stats[key]}"