# test_final_state.py

import os
import csv
from collections import defaultdict

def test_analyze_graph_cpp_exists():
    cpp_path = "/home/user/analyze_graph.cpp"
    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} does not exist."
    assert os.path.isfile(cpp_path), f"Path {cpp_path} is not a file."

def test_top_nodes_output():
    csv_path = "/home/user/network_events.csv"
    output_path = "/home/user/top_nodes.txt"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

    # Parse the CSV to compute the expected result dynamically
    edge_latest_event = {}

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = int(row["timestamp"])
            n1 = int(row["node1"])
            n2 = int(row["node2"])
            action = row["action"].strip().upper()

            u, v = min(n1, n2), max(n1, n2)

            if (u, v) not in edge_latest_event:
                edge_latest_event[(u, v)] = (ts, action)
            else:
                if ts > edge_latest_event[(u, v)][0]:
                    edge_latest_event[(u, v)] = (ts, action)

    # Reconstruct active graph
    degrees = defaultdict(int)
    for (u, v), (ts, action) in edge_latest_event.items():
        if action == "CONNECT":
            degrees[u] += 1
            degrees[v] += 1

    # Sort by degree (descending), then node_id (ascending)
    sorted_nodes = sorted(degrees.items(), key=lambda x: (-x[1], x[0]))
    top_5 = sorted_nodes[:5]

    expected_lines = [f"{node},{degree}" for node, degree in top_5]

    # Read actual output
    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 5, f"Expected exactly 5 lines in {output_path}, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."