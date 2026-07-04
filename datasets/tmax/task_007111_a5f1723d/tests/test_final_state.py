# test_final_state.py

import os
import csv
import math
import pytest

def compute_expected_anomalies(csv_path):
    if not os.path.isfile(csv_path):
        return []

    buckets = {}
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = int(row['timestamp'])
            cpu = float(row['cpu'])
            mem = float(row['mem'])
            net_in = float(row['net_in'])
            net_out = float(row['net_out'])

            bucket_idx = ts // 60
            if bucket_idx not in buckets:
                buckets[bucket_idx] = {'cpu': [], 'mem': [], 'net_in': [], 'net_out': []}

            buckets[bucket_idx]['cpu'].append(cpu)
            buckets[bucket_idx]['mem'].append(mem)
            buckets[bucket_idx]['net_in'].append(net_in)
            buckets[bucket_idx]['net_out'].append(net_out)

    sorted_indices = sorted(buckets.keys())

    anomalies = []
    prev_norm = None

    for idx in sorted_indices:
        b = buckets[idx]
        avg_cpu = sum(b['cpu']) / len(b['cpu'])
        avg_mem = sum(b['mem']) / len(b['mem'])
        avg_net_in = sum(b['net_in']) / len(b['net_in'])
        avg_net_out = sum(b['net_out']) / len(b['net_out'])

        norm = (
            avg_cpu / 100.0,
            avg_mem / 16000.0,
            avg_net_in / 1000.0,
            avg_net_out / 1000.0
        )

        if prev_norm is not None:
            dist = math.sqrt(
                (norm[0] - prev_norm[0])**2 +
                (norm[1] - prev_norm[1])**2 +
                (norm[2] - prev_norm[2])**2 +
                (norm[3] - prev_norm[3])**2
            )

            if dist > 0.4:
                bucket_start = idx * 60
                anomalies.append(f"[LOG] Anomaly detected at bucket {bucket_start}: distance={dist:.4f}")

        prev_norm = norm

    return anomalies

def test_anomalies_log_exists_and_correct():
    csv_path = '/home/user/system_metrics.csv'
    log_path = '/home/user/anomalies.log'

    assert os.path.isfile(csv_path), f"Input CSV file {csv_path} is missing."
    assert os.path.isfile(log_path), f"Output log file {log_path} was not generated."

    expected_lines = compute_expected_anomalies(csv_path)

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {log_path} do not match expected anomalies.\n"
        f"Expected: {expected_lines}\n"
        f"Actual:   {actual_lines}"
    )

def test_cpp_source_exists():
    cpp_path = '/home/user/detector.cpp'
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."