# test_final_state.py

import os
import csv
from datetime import datetime, timezone
import re

def test_c_source_file_exists():
    path = "/home/user/process_logs.c"
    assert os.path.exists(path), f"C source file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a regular file."

def test_c_executable_exists():
    path = "/home/user/process_logs"
    assert os.path.exists(path), f"Compiled executable {path} is missing."
    assert os.path.isfile(path), f"{path} is not a regular file."
    assert os.access(path, os.X_OK), f"Compiled file {path} is not executable."

def test_csv_output_exists():
    path = "/home/user/sampled_metrics.csv"
    assert os.path.exists(path), f"Output CSV {path} is missing."
    assert os.path.isfile(path), f"{path} is not a regular file."

def test_csv_output_content():
    raw_logs_path = "/home/user/raw_logs.txt"
    csv_path = "/home/user/sampled_metrics.csv"

    assert os.path.exists(raw_logs_path), "Raw logs file missing, cannot compute expected state."
    assert os.path.exists(csv_path), "CSV file missing, cannot verify content."

    # Compute expected results dynamically
    expected_data = {}
    with open(raw_logs_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: YYYY-MM-DD HH:MM:SS | REGION | [UTF-8 Message] CPU:[XX]%
            # Example: 2023-10-01 14:02:15 | JP | サーバーのステータスは正常です CPU:45%
            parts = line.split('|')
            if len(parts) < 3:
                continue

            time_str = parts[0].strip()
            region = parts[1].strip()
            message = parts[2].strip()

            # Parse timestamp to UTC epoch
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            epoch = int(dt.timestamp())

            # Calculate 10-minute window epoch
            window_epoch = epoch - (epoch % 600)

            # Extract CPU
            cpu_match = re.search(r'CPU:(\d+)%', message)
            if not cpu_match:
                continue
            cpu = int(cpu_match.group(1))

            key = (window_epoch, region)
            if key not in expected_data:
                expected_data[key] = cpu

    expected_rows = set()
    for (window_epoch, region), cpu in expected_data.items():
        expected_rows.add((str(window_epoch), region, str(cpu)))

    # Read actual CSV
    actual_rows = set()
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["WindowEpoch", "Region", "CPU_Percent"], f"CSV header is incorrect. Got: {header}"

        for row in reader:
            if not row:
                continue
            assert len(row) == 3, f"Invalid row format in CSV: {row}"
            actual_rows.add(tuple(row))

    # Compare
    missing = expected_rows - actual_rows
    extra = actual_rows - expected_rows

    error_msg = []
    if missing:
        error_msg.append(f"Missing expected rows: {missing}")
    if extra:
        error_msg.append(f"Unexpected extra rows: {extra}")

    assert not missing and not extra, "\n".join(error_msg)