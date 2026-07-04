# test_final_state.py

import os
import math
import csv

def compute_expected_report():
    a_path = '/home/user/sensor_a.csv'
    b_path = '/home/user/sensor_b.csv'

    a_data = []
    b_data = []

    with open(a_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            a_data.append((int(row['timestamp']), float(row['temperature'])))

    with open(b_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            b_data.append((int(row['timestamp']), float(row['temperature'])))

    min_ts = min(min(x[0] for x in a_data), min(x[0] for x in b_data))
    max_ts = max(max(x[0] for x in a_data), max(x[0] for x in b_data))

    start_time = (min_ts // 600) * 600
    if max_ts % 600 == 0:
        end_time = max_ts
    else:
        end_time = ((max_ts // 600) + 1) * 600

    num_buckets = (end_time - start_time) // 600

    def aggregate(data):
        buckets = [[] for _ in range(num_buckets)]
        for ts, temp in data:
            if start_time <= ts < end_time:
                idx = (ts - start_time) // 600
                buckets[idx].append(temp)

        means = [sum(b)/len(b) if b else None for b in buckets]

        # fill gaps
        # forward fill first, but handle leading gaps with backward fill
        # find first non-None
        first_valid = next((i for i, v in enumerate(means) if v is not None), None)
        if first_valid is not None:
            # backward fill leading gaps
            for i in range(first_valid):
                means[i] = means[first_valid]

            # forward fill remaining
            for i in range(first_valid + 1, num_buckets):
                if means[i] is None:
                    means[i] = means[i-1]

        return means

    agg_a = aggregate(a_data)
    agg_b = aggregate(b_data)

    def z_score(arr):
        n = len(arr)
        if n == 0: return arr
        mean = sum(arr) / n
        variance = sum((x - mean)**2 for x in arr) / n
        std = math.sqrt(variance)
        if std == 0:
            return [0.0] * n
        return [(x - mean) / std for x in arr]

    norm_a = z_score(agg_a)
    norm_b = z_score(agg_b)

    dist = math.sqrt(sum((a - b)**2 for a, b in zip(norm_a, norm_b)))

    return num_buckets, dist

def test_drift_analyzer_compiled():
    assert os.path.exists('/home/user/drift_analyzer.cpp'), "Source file drift_analyzer.cpp is missing."
    assert os.path.exists('/home/user/drift_analyzer'), "Compiled executable drift_analyzer is missing."
    assert os.access('/home/user/drift_analyzer', os.X_OK), "drift_analyzer is not executable."

def test_drift_report_output():
    report_path = '/home/user/drift_report.txt'
    assert os.path.exists(report_path), f"Output file {report_path} is missing."

    expected_buckets, expected_dist = compute_expected_report()

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, found {len(lines)}."
    assert lines[0] == f"Total Buckets: {expected_buckets}", f"Line 1 mismatch. Expected 'Total Buckets: {expected_buckets}', got '{lines[0]}'."

    expected_dist_str = f"Euclidean Distance: {expected_dist:.4f}"
    assert lines[1] == expected_dist_str, f"Line 2 mismatch. Expected '{expected_dist_str}', got '{lines[1]}'."