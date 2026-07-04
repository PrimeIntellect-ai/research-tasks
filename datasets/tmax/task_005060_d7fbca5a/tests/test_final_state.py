# test_final_state.py

import os
import csv
import math
from datetime import datetime, timezone
from collections import defaultdict
import pytest

# Paths
RAW_LOGS_DIR = "/home/user/logs/raw"
ANOMALIES_CSV = "/home/user/logs/anomalies.csv"
SCRIPT_PATH = "/home/user/analyze_logs.py"

def compute_expected_anomalies():
    logs = []
    stats = defaultdict(list)

    for file in os.listdir(RAW_LOGS_DIR):
        if not file.endswith(".log"):
            continue
        with open(os.path.join(RAW_LOGS_DIR, file), "r") as f:
            for line in f:
                parts = line.strip().split("] ")
                if len(parts) != 2:
                    continue
                ts_str = parts[0][1:]
                rest = parts[1].split(" ")
                ip = rest[0]
                endpoint = rest[2]
                rt = int(rest[4])

                dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                # Accept both strict UTC epoch and local epoch to be robust against timezone interpretations
                epoch_utc = int(dt.replace(tzinfo=timezone.utc).timestamp())
                epoch_local = int(dt.timestamp())

                logs.append((epoch_utc, epoch_local, ip, endpoint, rt))
                stats[endpoint].append(rt)

    agg = {}
    for ep, times in stats.items():
        n = len(times)
        if n < 2:
            continue
        mean = sum(times) / n
        variance = sum((x - mean) ** 2 for x in times) / (n - 1)
        std = math.sqrt(variance)
        agg[ep] = (mean, std)

    anomalies_utc = []
    anomalies_local = []

    for epoch_utc, epoch_local, ip, endpoint, rt in logs:
        if endpoint in agg:
            mean, std = agg[endpoint]
            if std > 0:
                z = (rt - mean) / std
                if z > 3.0:
                    z_str = f"{z:.3f}"
                    anomalies_utc.append([str(epoch_utc), ip, endpoint, str(rt), z_str])
                    anomalies_local.append([str(epoch_local), ip, endpoint, str(rt), z_str])

    anomalies_utc.sort(key=lambda x: (int(x[0]), x[1]))
    anomalies_local.sort(key=lambda x: (int(x[0]), x[1]))

    return anomalies_utc, anomalies_local

def test_script_exists_and_uses_multiprocessing():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "multiprocessing" in content or "concurrent.futures" in content, \
        "Script must use multiprocessing or concurrent.futures as per the instructions."

def test_anomalies_csv_exists():
    assert os.path.isfile(ANOMALIES_CSV), f"Output file {ANOMALIES_CSV} does not exist."

def test_anomalies_csv_content():
    expected_utc, expected_local = compute_expected_anomalies()

    with open(ANOMALIES_CSV, "r", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("The anomalies CSV is empty.")

        expected_header = ["timestamp_epoch", "ip_address", "endpoint", "response_time_ms", "z_score"]
        assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_utc), \
        f"Row count mismatch. Expected {len(expected_utc)} anomalies, got {len(actual_rows)}."

    # Check if the rows match either the strict UTC interpretation or the local naive interpretation
    match_utc = True
    match_local = True

    for actual, exp_utc, exp_loc in zip(actual_rows, expected_utc, expected_local):
        if actual != exp_utc:
            match_utc = False
        if actual != exp_loc:
            match_local = False

    assert match_utc or match_local, \
        "The anomalies output does not match the expected values. Check your Z-score calculations, filtering, and sorting."