# test_final_state.py

import os
import csv
import stat
import pytest
from collections import defaultdict

RAW_FILE = "/home/user/raw_telemetry.csv"
PROCESSED_FILE = "/home/user/processed_telemetry.csv"
SCRIPT_FILE = "/home/user/process_telemetry.sh"

def compute_expected_telemetry(raw_path):
    # Parse raw data
    # region -> minute_epoch -> { 'latencies': [], 'chars': 0 }
    data = defaultdict(lambda: defaultdict(lambda: {'latencies': [], 'chars': 0}))

    with open(raw_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            epoch_sec = int(row[0])
            region = row[1]
            latency = float(row[2])
            error_msg = row[3] if len(row) > 3 else ""

            minute_epoch = (epoch_sec // 60) * 60
            data[region][minute_epoch]['latencies'].append(latency)
            data[region][minute_epoch]['chars'] += len(error_msg)

    expected_rows = []

    # Process per region
    for region in sorted(data.keys()):
        region_data = data[region]
        min_epoch = min(region_data.keys())
        max_epoch = max(region_data.keys())

        # Fill gaps and compute rolling average
        current_epoch = min_epoch
        last_latency = None
        history = []

        while current_epoch <= max_epoch:
            if current_epoch in region_data:
                latencies = region_data[current_epoch]['latencies']
                mean_latency = sum(latencies) / len(latencies)
                chars = region_data[current_epoch]['chars']
                last_latency = mean_latency
            else:
                mean_latency = last_latency
                chars = 0

            history.append(mean_latency)
            if len(history) > 5:
                history.pop(0)

            rolling_avg = sum(history) / len(history)

            expected_rows.append(
                f"{current_epoch},{region},{mean_latency:.2f},{rolling_avg:.2f},{chars}"
            )

            current_epoch += 60

    return expected_rows

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_FILE), f"Script {SCRIPT_FILE} does not exist."
    st = os.stat(SCRIPT_FILE)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_FILE} is not executable."

def test_processed_file_exists():
    assert os.path.exists(PROCESSED_FILE), f"Output file {PROCESSED_FILE} does not exist. Did the script run?"
    assert os.path.isfile(PROCESSED_FILE), f"Path {PROCESSED_FILE} is not a file."

def test_processed_telemetry_content():
    assert os.path.exists(RAW_FILE), f"Raw file {RAW_FILE} is missing, cannot verify."

    expected_lines = compute_expected_telemetry(RAW_FILE)

    with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows, but got {len(actual_lines)} in {PROCESSED_FILE}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Mismatch at row {i+1}.\nExpected: {expected}\nActual:   {actual}"