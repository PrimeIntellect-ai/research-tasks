# test_final_state.py
import os
import csv
from datetime import datetime, timezone

def test_worker_threads_ma_output():
    log_file_path = "/home/user/config_audit.log"
    output_file_path = "/home/user/worker_threads_ma.csv"

    assert os.path.isfile(output_file_path), f"The output file {output_file_path} is missing."

    # Recompute expected output
    expected_rows = []
    window = []

    with open(log_file_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 6:
                continue

            timestamp_str, user, server, config_key, old_val, new_val = parts

            if config_key == "worker_threads":
                new_val = int(new_val)
                window.append(new_val)

                if len(window) >= 3:
                    # Mathematical rounding (half up)
                    avg = sum(window[-3:]) / 3.0
                    rounded_avg = int(avg + 0.5)

                    # Convert timestamp to epoch
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
                    dt = dt.replace(tzinfo=timezone.utc)
                    epoch = int(dt.timestamp())

                    expected_rows.append([str(epoch), server, str(rounded_avg)])

    # Read actual output
    actual_rows = []
    with open(output_file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."