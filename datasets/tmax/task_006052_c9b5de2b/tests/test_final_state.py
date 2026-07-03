# test_final_state.py

import os
import csv
import datetime
from collections import defaultdict

def parse_eu_time(t_str):
    dt = datetime.datetime.strptime(t_str, "%d/%m/%Y %H:%M:%S")
    return int(dt.replace(tzinfo=datetime.timezone.utc).timestamp())

def parse_us_time(t_str):
    dt = datetime.datetime.strptime(t_str, "%Y-%m-%dT%H:%M:%SZ")
    return int(dt.replace(tzinfo=datetime.timezone.utc).timestamp())

def parse_asia_time(t_str):
    return int(t_str) // 1000

def compute_expected_anomalies():
    raw_logs_dir = "/home/user/raw_logs"
    eu_log = os.path.join(raw_logs_dir, "server_eu.log")
    us_log = os.path.join(raw_logs_dir, "server_us.log")
    asia_log = os.path.join(raw_logs_dir, "server_asia.log")

    entries = []

    if os.path.exists(eu_log):
        with open(eu_log, 'r', encoding='iso-8859-1') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = [p.strip() for p in line.split('|')]
                epoch = parse_eu_time(parts[0])
                latency_ms = float(parts[2])
                entries.append((epoch, latency_ms))

    if os.path.exists(us_log):
        with open(us_log, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = [p.strip() for p in line.split('|')]
                epoch = parse_us_time(parts[0])
                latency_ms = float(parts[2]) * 1000.0
                entries.append((epoch, latency_ms))

    if os.path.exists(asia_log):
        with open(asia_log, 'r', encoding='utf-16le') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = [p.strip() for p in line.split('|')]
                epoch = parse_asia_time(parts[0])
                latency_ms = float(parts[2]) / 1000.0
                entries.append((epoch, latency_ms))

    buckets = defaultdict(list)
    for epoch, lat in entries:
        bucket_start = (epoch // 300) * 300
        buckets[bucket_start].append(lat)

    bucket_means = {}
    for b_start, lats in buckets.items():
        bucket_means[b_start] = sum(lats) / len(lats)

    sorted_buckets = sorted(bucket_means.keys())

    anomalies = []
    for i in range(1, len(sorted_buckets)):
        curr_b = sorted_buckets[i]
        prev_b = sorted_buckets[i-1]
        curr_mean = bucket_means[curr_b]
        prev_mean = bucket_means[prev_b]

        if curr_mean > 2.5 * prev_mean:
            anomalies.append({
                'bucket_start_epoch': str(curr_b),
                'avg_latency_ms': f"{curr_mean:.2f}",
                'prev_avg_latency_ms': f"{prev_mean:.2f}"
            })

    return anomalies

def test_anomalies_csv_exists():
    csv_path = "/home/user/anomalies.csv"
    assert os.path.isfile(csv_path), f"Expected output file {csv_path} does not exist."

def test_anomalies_csv_content():
    csv_path = "/home/user/anomalies.csv"
    assert os.path.isfile(csv_path), f"Expected output file {csv_path} does not exist."

    expected_anomalies = compute_expected_anomalies()

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['bucket_start_epoch', 'avg_latency_ms', 'prev_avg_latency_ms'], \
            f"CSV header is incorrect. Expected ['bucket_start_epoch', 'avg_latency_ms', 'prev_avg_latency_ms'], got {reader.fieldnames}"

        rows = list(reader)

    assert len(rows) == len(expected_anomalies), \
        f"Expected {len(expected_anomalies)} anomalies, but found {len(rows)} in the CSV."

    for i, (expected, actual) in enumerate(zip(expected_anomalies, rows)):
        assert actual['bucket_start_epoch'] == expected['bucket_start_epoch'], \
            f"Row {i+1}: Expected bucket_start_epoch {expected['bucket_start_epoch']}, got {actual['bucket_start_epoch']}"
        assert actual['avg_latency_ms'] == expected['avg_latency_ms'], \
            f"Row {i+1}: Expected avg_latency_ms {expected['avg_latency_ms']}, got {actual['avg_latency_ms']}"
        assert actual['prev_avg_latency_ms'] == expected['prev_avg_latency_ms'], \
            f"Row {i+1}: Expected prev_avg_latency_ms {expected['prev_avg_latency_ms']}, got {actual['prev_avg_latency_ms']}"