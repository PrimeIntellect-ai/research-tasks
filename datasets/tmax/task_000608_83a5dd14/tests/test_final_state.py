# test_final_state.py
import os
import csv
import pytest

def compute_expected_summary(input_path):
    # Read data
    data = []
    with open(input_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'timestamp': int(row['timestamp']),
                'server_id': row['server_id'],
                'cpu_temp': float(row['cpu_temp']) if row['cpu_temp'] else None,
                'latency_ms': float(row['latency_ms']) if row['latency_ms'] else None
            })

    # Group by server_id
    servers = {}
    for row in data:
        servers.setdefault(row['server_id'], []).append(row)

    expected_summary = {}

    for srv, records in servers.items():
        # Sort chronologically
        records.sort(key=lambda x: x['timestamp'])

        # Interpolate cpu_temp
        for i, rec in enumerate(records):
            if rec['cpu_temp'] is None:
                # Find previous valid
                prev_idx = i - 1
                while prev_idx >= 0 and records[prev_idx]['cpu_temp'] is None:
                    prev_idx -= 1

                # Find next valid
                next_idx = i + 1
                while next_idx < len(records) and records[next_idx]['cpu_temp'] is None:
                    next_idx += 1

                prev_rec = records[prev_idx]
                next_rec = records[next_idx]

                time_diff = next_rec['timestamp'] - prev_rec['timestamp']
                temp_diff = next_rec['cpu_temp'] - prev_rec['cpu_temp']

                interpolated_temp = prev_rec['cpu_temp'] + temp_diff * ((rec['timestamp'] - prev_rec['timestamp']) / time_diff)
                rec['cpu_temp'] = interpolated_temp

        # Calculate mean latency
        valid_lats = [r['latency_ms'] for r in records if r['latency_ms'] is not None]
        mean_lat = sum(valid_lats) / len(valid_lats) if valid_lats else 0.0

        # Replace missing latency
        for rec in records:
            if rec['latency_ms'] is None:
                rec['latency_ms'] = mean_lat

        # Calculate metrics
        max_temp = max(r['cpu_temp'] for r in records)
        avg_latency = sum(r['latency_ms'] for r in records) / len(records)
        overheat_events = sum(1 for r in records if r['cpu_temp'] > 85.0)

        expected_summary[srv] = {
            'max_temp': f"{max_temp:.2f}",
            'avg_latency': f"{avg_latency:.2f}",
            'overheat_events': str(overheat_events)
        }

    return expected_summary

def test_server_summary_exists():
    path = "/home/user/server_summary.csv"
    assert os.path.exists(path), f"Output file {path} was not created."
    assert os.path.isfile(path), f"{path} is not a file."

def test_server_summary_contents():
    input_path = "/home/user/sensor_logs.csv"
    output_path = "/home/user/server_summary.csv"

    expected_summary = compute_expected_summary(input_path)

    actual_data = []
    with open(output_path, 'r') as f:
        reader = csv.DictReader(f)
        actual_headers = reader.fieldnames
        for row in reader:
            actual_data.append(row)

    expected_headers = ['server_id', 'max_temp', 'avg_latency', 'overheat_events']
    assert actual_headers == expected_headers, f"Expected headers {expected_headers}, but got {actual_headers}"

    # Check sorting
    actual_servers = [row['server_id'] for row in actual_data]
    assert actual_servers == sorted(actual_servers), "The rows in the output CSV are not sorted alphabetically by server_id."

    # Check contents
    assert len(actual_data) == len(expected_summary), f"Expected {len(expected_summary)} rows, but got {len(actual_data)}"

    for row in actual_data:
        srv = row['server_id']
        assert srv in expected_summary, f"Unexpected server_id {srv} in output."
        expected = expected_summary[srv]

        assert row['max_temp'] == expected['max_temp'], f"For server {srv}, expected max_temp {expected['max_temp']}, got {row['max_temp']}"
        assert row['avg_latency'] == expected['avg_latency'], f"For server {srv}, expected avg_latency {expected['avg_latency']}, got {row['avg_latency']}"
        assert row['overheat_events'] == expected['overheat_events'], f"For server {srv}, expected overheat_events {expected['overheat_events']}, got {row['overheat_events']}"