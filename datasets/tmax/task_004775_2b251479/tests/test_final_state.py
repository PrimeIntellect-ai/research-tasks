# test_final_state.py

import os
import json
import csv
import re
from collections import defaultdict

def compute_expected_deadlocks():
    tx_locks_path = "/home/user/tx_locks.json"
    resource_graph_path = "/home/user/resource_graph.nt"

    assert os.path.exists(tx_locks_path), f"Missing {tx_locks_path}"
    assert os.path.exists(resource_graph_path), f"Missing {resource_graph_path}"

    with open(tx_locks_path, 'r') as f:
        locks = json.load(f)

    granted = defaultdict(list)
    waiting = defaultdict(list)

    for lock in locks:
        tx_id = lock['tx_id']
        res = lock['resource']
        state = lock['state']
        ts = lock['timestamp']
        if state == 'GRANTED':
            granted[res].append((tx_id, ts))
        elif state == 'WAITING':
            waiting[tx_id].append((res, ts))

    depends_on = defaultdict(list)
    with open(resource_graph_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Parse <R10> <dependsOn> <R15> .
            match = re.match(r'<([^>]+)>\s+<dependsOn>\s+<([^>]+)>\s*\.', line)
            if match:
                depends_on[match.group(1)].append(match.group(2))

    deadlocks = {}

    for tx_a, a_waits in waiting.items():
        for res1, ts_a_wait in a_waits:
            for res2 in depends_on.get(res1, []):
                for tx_b, ts_b_grant in granted.get(res2, []):
                    if tx_a == tx_b:
                        continue

                    # Now check if tx_b is waiting for res3 which depends on res4 granted to tx_a
                    for res3, ts_b_wait in waiting.get(tx_b, []):
                        for res4 in depends_on.get(res3, []):
                            for tx_a_check, ts_a_grant in granted.get(res4, []):
                                if tx_a_check == tx_a:
                                    # Deadlock found!
                                    tx_1, tx_2 = sorted([tx_a, tx_b])
                                    min_ts = min(ts_a_wait, ts_b_grant, ts_b_wait, ts_a_grant)
                                    pair = (tx_1, tx_2)
                                    if pair not in deadlocks or min_ts < deadlocks[pair]:
                                        deadlocks[pair] = min_ts

    sorted_deadlocks = sorted(deadlocks.items(), key=lambda x: (x[1], x[0][0]))
    top_5 = sorted_deadlocks[:5]

    return [(k[0], k[1], str(v)) for k, v in top_5]

def test_deadlocks_report_exists_and_correct():
    report_path = "/home/user/deadlocks_report.csv"
    assert os.path.exists(report_path), f"The output file {report_path} was not created."

    expected_data = compute_expected_deadlocks()

    with open(report_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"{report_path} is empty."

        assert header == ['tx_1', 'tx_2', 'min_timestamp'], \
            f"CSV header is incorrect. Expected ['tx_1', 'tx_2', 'min_timestamp'], got {header}"

        rows = list(reader)

    assert len(rows) == len(expected_data), \
        f"Expected {len(expected_data)} rows in the report (excluding header), but found {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_data)):
        assert len(actual) == 3, f"Row {i+1} does not have exactly 3 columns: {actual}"
        assert actual[0] == expected[0], f"Row {i+1} tx_1 mismatch: expected {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"Row {i+1} tx_2 mismatch: expected {expected[1]}, got {actual[1]}"
        assert actual[2] == expected[2], f"Row {i+1} min_timestamp mismatch: expected {expected[2]}, got {actual[2]}"