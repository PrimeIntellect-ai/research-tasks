# test_final_state.py

import os
import csv
import re
import pytest

def compute_expected_changepoints(input_path):
    if not os.path.isfile(input_path):
        pytest.fail(f"Input file {input_path} is missing, cannot compute expected state.")

    # Read and parse input
    data = []
    with open(input_path, 'r') as f:
        for line in f:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) != 4:
                continue
            timestamp = int(parts[0])
            server_id = parts[1]
            raw_log = parts[2]
            cpu_limit_str = parts[3]

            # Regex extraction
            match = re.search(r"hash=\[([a-zA-Z0-9]{6})\]", raw_log)
            config_hash = match.group(1) if match else ""

            cpu_limit = float(cpu_limit_str) if cpu_limit_str else None

            data.append({
                'timestamp': timestamp,
                'server_id': server_id,
                'config_hash': config_hash,
                'cpu_limit': cpu_limit
            })

    # Group by server_id
    servers = {}
    for row in data:
        servers.setdefault(row['server_id'], []).append(row)

    expected_rows = []

    for server_id in sorted(servers.keys()):
        # Sort by timestamp ascending
        server_data = sorted(servers[server_id], key=lambda x: x['timestamp'])

        # Interpolate missing cpu_limit
        for i, row in enumerate(server_data):
            if row['cpu_limit'] is None:
                # Find preceding
                t0, v0 = None, None
                for prev_row in reversed(server_data[:i]):
                    if prev_row['cpu_limit'] is not None:
                        t0, v0 = prev_row['timestamp'], prev_row['cpu_limit']
                        break

                # Find succeeding
                t1, v1 = None, None
                for next_row in server_data[i+1:]:
                    if next_row['cpu_limit'] is not None:
                        t1, v1 = next_row['timestamp'], next_row['cpu_limit']
                        break

                if t0 is not None and t1 is not None and t1 != t0:
                    row['cpu_limit'] = v0 + (v1 - v0) * (row['timestamp'] - t0) / (t1 - t0)

        # Deduplicate (Changepoint Detection)
        prev_hash = None
        prev_cpu = None

        for row in server_data:
            curr_hash = row['config_hash']
            curr_cpu = round(row['cpu_limit'], 2) if row['cpu_limit'] is not None else None

            if prev_hash is None:
                expected_rows.append(row)
                prev_hash = curr_hash
                prev_cpu = curr_cpu
            else:
                if curr_hash != prev_hash or curr_cpu != prev_cpu:
                    expected_rows.append(row)
                    prev_hash = curr_hash
                    prev_cpu = curr_cpu

    # Format expected output
    expected_output = [["timestamp", "server_id", "config_hash", "cpu_limit"]]
    for row in expected_rows:
        cpu_formatted = f"{row['cpu_limit']:.2f}" if row['cpu_limit'] is not None else ""
        expected_output.append([str(row['timestamp']), row['server_id'], row['config_hash'], cpu_formatted])

    return expected_output

def test_changepoints_csv_exists():
    """Check that the output CSV file exists."""
    path = "/home/user/changepoints.csv"
    assert os.path.isfile(path), f"Output file {path} is missing. Did your Rust program run successfully?"

def test_changepoints_csv_content():
    """Check that the output CSV matches the expected computed changepoints."""
    input_path = "/home/user/raw_configs.txt"
    output_path = "/home/user/changepoints.csv"

    expected_data = compute_expected_changepoints(input_path)

    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    actual_data = []
    with open(output_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_data.append(row)

    assert len(actual_data) > 0, f"The file {output_path} is empty."

    # Check header
    assert actual_data[0] == ["timestamp", "server_id", "config_hash", "cpu_limit"], \
        f"CSV header in {output_path} is incorrect. Expected {expected_data[0]}, got {actual_data[0]}."

    # Check row counts
    assert len(actual_data) == len(expected_data), \
        f"Row count mismatch. Expected {len(expected_data)} rows (including header), got {len(actual_data)}."

    # Check content row by row
    for i in range(1, len(expected_data)):
        exp_row = expected_data[i]
        act_row = actual_data[i]
        assert act_row == exp_row, \
            f"Mismatch at row {i+1}. Expected {exp_row}, got {act_row}."