# test_final_state.py

import os
import re
import csv
from datetime import datetime
import pytest

LOG_PATH = '/home/user/system_events.log'
SCRIPT_PATH = '/home/user/process.sh'
OUTPUT_CSV = '/home/user/metrics_summary.csv'

def compute_expected_csv():
    if not os.path.exists(LOG_PATH):
        pytest.fail(f"Required log file {LOG_PATH} is missing.")

    seen_hashes = set()
    aggregated = {}  # (bucket, service, metric) -> max_val

    pattern = re.compile(r'^\[(.*?)\] SVC:(.*?) DEDUPE:(.*?) METRICS:(.*)$')

    with open(LOG_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if not match:
                continue

            ts_str, service, dedupe_hash, metrics_str = match.groups()

            if dedupe_hash in seen_hashes:
                continue
            seen_hashes.add(dedupe_hash)

            dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            bucket_minute = (dt.minute // 15) * 15
            bucket_dt = dt.replace(minute=bucket_minute, second=0)
            bucket_str = bucket_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            metrics = metrics_str.split(',')
            for m in metrics:
                if '=' not in m:
                    continue
                k, v = m.split('=', 1)
                val = float(v) if '.' in v else int(v)

                key = (bucket_str, service, k)
                if key not in aggregated or val > aggregated[key]:
                    aggregated[key] = val

    sorted_keys = sorted(aggregated.keys())

    expected_rows = [["bucket", "service", "metric", "max_value"]]
    for k in sorted_keys:
        expected_rows.append([k[0], k[1], k[2], str(aggregated[k])])

    return expected_rows

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_output_csv_exists():
    assert os.path.exists(OUTPUT_CSV), f"Output file {OUTPUT_CSV} does not exist."
    assert os.path.isfile(OUTPUT_CSV), f"{OUTPUT_CSV} is not a file."

def test_output_csv_content():
    expected_data = compute_expected_csv()

    actual_data = []
    with open(OUTPUT_CSV, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_data.append(row)

    assert len(actual_data) > 0, f"{OUTPUT_CSV} is empty."
    assert actual_data[0] == expected_data[0], f"Header mismatch. Expected {expected_data[0]}, got {actual_data[0]}"

    assert len(actual_data) == len(expected_data), f"Row count mismatch. Expected {len(expected_data)} rows (including header), got {len(actual_data)}"

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Row {i} mismatch. Expected {expected}, got {actual}"