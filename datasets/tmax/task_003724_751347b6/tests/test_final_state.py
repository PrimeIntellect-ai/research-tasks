# test_final_state.py

import os
import json
from collections import Counter

def test_top_nodes_csv():
    jsonl_path = "/home/user/transactions.jsonl"
    csv_path = "/home/user/top_nodes.csv"

    assert os.path.exists(jsonl_path), f"Input file missing: {jsonl_path}"
    assert os.path.exists(csv_path), f"Output file missing: {csv_path}"

    # Recompute the expected top 3 nodes from the input data
    receivers = Counter()
    with open(jsonl_path, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    if 'receiver' in data:
                        receivers[data['receiver']] += 1
                except json.JSONDecodeError:
                    continue

    # Sort by in_degree (descending), then node_id (ascending)
    sorted_nodes = sorted(receivers.items(), key=lambda x: (-x[1], x[0]))
    top_3 = sorted_nodes[:3]

    expected_lines = [f"{node},{count}" for node, count in top_3]

    # Read actual output
    with open(csv_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in CSV, got {len(actual_lines)}"

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Row {i+1} mismatch: expected '{expected}', got '{actual}'"