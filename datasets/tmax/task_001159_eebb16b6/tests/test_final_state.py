# test_final_state.py
import os
import csv
from collections import defaultdict

def test_source_code_and_executable_exist():
    """Check that the C++ source code and the compiled executable exist."""
    assert os.path.isfile("/home/user/graph_analyzer.cpp"), "Source file /home/user/graph_analyzer.cpp is missing."
    assert os.path.isfile("/home/user/graph_analyzer"), "Executable /home/user/graph_analyzer is missing."
    assert os.access("/home/user/graph_analyzer", os.X_OK), "/home/user/graph_analyzer is not executable."

def test_component_result_correctness():
    """Verify the contents of component_result.txt by recomputing the logic from the CSV."""
    csv_path = "/home/user/network.csv"
    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."

    # Step 1: Read data and group by source
    transactions = defaultdict(list)
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions[row["source"]].append({
                "target": row["target"],
                "amount": float(row["amount"]),
                "time_seq": int(row["time_seq"])
            })

    # Step 2: Compute cumulative sum and filter edges
    edges = []
    for source, txs in transactions.items():
        # sort by time_seq ascending
        txs.sort(key=lambda x: x["time_seq"])
        cum_sum = 0.0
        for tx in txs:
            cum_sum += tx["amount"]
            if cum_sum > 150.0:
                edges.append((source, tx["target"]))

    # Step 3: Compute connected components
    adj = defaultdict(set)
    nodes = set()
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
        nodes.add(u)
        nodes.add(v)

    visited = set()
    components = []
    for node in nodes:
        if node not in visited:
            comp = []
            stack = [node]
            visited.add(node)
            while stack:
                curr = stack.pop()
                comp.append(curr)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            components.append(comp)

    # Step 4: Find the largest component
    if not components:
        expected_size = 0
        expected_nodes_str = ""
    else:
        # Sort components by size (descending), then by lexicographically smallest node
        components.sort(key=lambda c: (-len(c), min(c)))
        largest_comp = components[0]
        expected_size = len(largest_comp)
        expected_nodes_str = ",".join(sorted(largest_comp))

    result_path = "/home/user/component_result.txt"
    assert os.path.isfile(result_path), f"Output file {result_path} is missing."

    with open(result_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {result_path}, found {len(lines)}."

    actual_size = int(lines[0])
    actual_nodes_str = lines[1]

    assert actual_size == expected_size, f"Expected largest component size {expected_size}, got {actual_size}."
    assert actual_nodes_str == expected_nodes_str, f"Expected nodes '{expected_nodes_str}', got '{actual_nodes_str}'."