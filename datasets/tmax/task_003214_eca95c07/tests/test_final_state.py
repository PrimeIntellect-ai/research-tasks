# test_final_state.py

import os
import csv
from collections import defaultdict

def test_rolling_metrics_exists():
    """Test that the output CSV file exists."""
    file_path = "/home/user/rolling_metrics.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Did the script run?"

def test_rolling_metrics_contents():
    """Test that the output CSV file has the correctly computed rolling metrics."""
    input_file = "/home/user/server_logs.csv"
    output_file = "/home/user/rolling_metrics.csv"

    assert os.path.isfile(input_file), f"Input file {input_file} is missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    # 1. Dynamically compute the expected result from the input file
    server_data = defaultdict(list)
    with open(input_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            server_data[row["server_id"]].append({
                "timestamp": int(row["timestamp"]),
                "cpu_usage": row["cpu_usage"]
            })

    expected_rows = []
    for server_id, records in server_data.items():
        # Sort by timestamp ascending
        records.sort(key=lambda x: x["timestamp"])

        last_cpu = 0.0
        cpu_history = []

        for rec in records:
            # Impute missing cpu_usage
            if rec["cpu_usage"] == "":
                cpu = last_cpu
            else:
                cpu = float(rec["cpu_usage"])
                last_cpu = cpu

            cpu_history.append(cpu)

            # 3-period rolling average
            window = cpu_history[-3:]
            avg_cpu = sum(window) / len(window)

            expected_rows.append({
                "timestamp": str(rec["timestamp"]),
                "server_id": server_id,
                "rolling_cpu": f"{avg_cpu:.2f}"
            })

    # Sort expected output by timestamp ascending, then server_id ascending
    expected_rows.sort(key=lambda x: (int(x["timestamp"]), x["server_id"]))

    # 2. Read the actual output
    actual_rows = []
    with open(output_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["timestamp", "server_id", "rolling_cpu"], \
            f"Incorrect headers in {output_file}. Expected ['timestamp', 'server_id', 'rolling_cpu'], got {reader.fieldnames}"
        for row in reader:
            actual_rows.append(row)

    # 3. Compare actual vs expected
    assert len(actual_rows) == len(expected_rows), \
        f"Row count mismatch in {output_file}. Expected {len(expected_rows)} rows, got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, \
            f"Mismatch at row {i+1} (excluding header). Expected {expected}, got {actual}."