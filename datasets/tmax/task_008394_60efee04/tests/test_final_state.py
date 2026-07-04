# test_final_state.py

import os
import pytest
from collections import defaultdict

def test_fixed_timeline_csv_exists_and_correct():
    output_path = "/home/user/fixed_timeline.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. The C++ program may not have run successfully."

    # Recompute expected results from logs
    events = defaultdict(list)
    log_files = [
        "/home/user/logs/service_a.log",
        "/home/user/logs/service_b.log",
        "/home/user/logs/service_c.log"
    ]

    for log_path in log_files:
        assert os.path.isfile(log_path), f"Log file {log_path} is missing."
        with open(log_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    txn_id, ts = parts[0], float(parts[1])
                    events[txn_id].append(ts)

    expected_lines = ["txn_id,duration"]
    for txn_id in sorted(events.keys()):
        ts_list = sorted(events[txn_id])
        duration = ts_list[-1] - ts_list[0]
        expected_lines.append(f"{txn_id},{duration:.3f}")

    expected_content = "\n".join(expected_lines)

    with open(output_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {output_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{actual_content}\n\n"
        f"Ensure that the C++ program computes durations using double precision to avoid truncation."
    )