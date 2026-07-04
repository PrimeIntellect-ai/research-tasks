# test_final_state.py

import os
import math
import csv
import pytest

RAW_DATA_PATH = "/home/user/data/raw_data.csv"
PREPARED_DATA_PATH = "/home/user/data/prepared_data.csv"
METRICS_PATH = "/home/user/data/metrics.txt"

def compute_t_stats():
    with open(RAW_DATA_PATH, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Group data by label
        data_0 = {col: [] for col in header[2:]}
        data_1 = {col: [] for col in header[2:]}

        for row in reader:
            label = int(row[1])
            for i, col in enumerate(header[2:]):
                if label == 0:
                    data_0[col].append(float(row[i+2]))
                else:
                    data_1[col].append(float(row[i+2]))

    t_stats = []
    for col in header[2:]:
        n0 = len(data_0[col])
        n1 = len(data_1[col])

        mean0 = sum(data_0[col]) / n0
        mean1 = sum(data_1[col]) / n1

        var0 = sum((x - mean0)**2 for x in data_0[col]) / (n0 - 1)
        var1 = sum((x - mean1)**2 for x in data_1[col]) / (n1 - 1)

        t_stat = abs(mean1 - mean0) / math.sqrt((var1 / n1) + (var0 / n0))
        t_stats.append((col, t_stat))

    t_stats.sort(key=lambda x: x[1], reverse=True)
    return t_stats[:3]

def test_metrics_file():
    assert os.path.exists(METRICS_PATH), f"File {METRICS_PATH} does not exist."

    expected_top3 = compute_t_stats()

    with open(METRICS_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in {METRICS_PATH}, found {len(lines)}."

    for i, (expected_feat, expected_t) in enumerate(expected_top3):
        parts = lines[i].split(":")
        assert len(parts) == 2, f"Invalid format in {METRICS_PATH} on line {i+1}."
        feat = parts[0].strip()
        t_val = float(parts[1].strip())

        assert feat == expected_feat, f"Expected feature {expected_feat} at rank {i+1}, found {feat}."
        assert abs(t_val - expected_t) < 0.0005, f"Expected t-stat {expected_t:.4f} for {feat}, found {t_val}."

def test_prepared_data_file():
    assert os.path.exists(PREPARED_DATA_PATH), f"File {PREPARED_DATA_PATH} does not exist."

    expected_top3 = compute_t_stats()
    expected_header = f"id,label,{expected_top3[0][0]},{expected_top3[1][0]},{expected_top3[2][0]}"

    with open(PREPARED_DATA_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2001, f"Expected 2001 lines in {PREPARED_DATA_PATH}, found {len(lines)}."
    assert lines[0] == expected_header, f"Expected header '{expected_header}', found '{lines[0]}'."

    # Check class balance
    label_0_count = 0
    label_1_count = 0
    for line in lines[1:]:
        parts = line.split(",")
        label = int(parts[1])
        if label == 0:
            label_0_count += 1
        elif label == 1:
            label_1_count += 1

    assert label_0_count == 1000, f"Expected 1000 records for label 0, found {label_0_count}."
    assert label_1_count == 1000, f"Expected 1000 records for label 1, found {label_1_count}."