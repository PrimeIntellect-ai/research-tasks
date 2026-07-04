# test_final_state.py

import os
import csv
from collections import defaultdict

def test_node_metrics_exists():
    """Verify that the output file node_metrics.csv has been created."""
    assert os.path.isfile("/home/user/node_metrics.csv"), "The output file /home/user/node_metrics.csv does not exist."

def test_node_metrics_contents():
    """Verify that the node_metrics.csv contains the correct windowed top-K sum aggregation."""
    input_file = "/home/user/transactions.csv"
    output_file = "/home/user/node_metrics.csv"

    assert os.path.isfile(input_file), f"Input file {input_file} is missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    # 1. Compute expected results dynamically from the input file
    edges = defaultdict(int)
    nodes = set()

    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source = row['source']
            target = row['target']
            amount = int(row['amount'])

            nodes.add(source)
            nodes.add(target)

            # Deduplication: keep max amount
            if amount > edges[(source, target)]:
                edges[(source, target)] = amount

    # Group incoming edges by target
    incoming = defaultdict(list)
    for (source, target), amount in edges.items():
        incoming[target].append(amount)

    expected_metrics = {}
    for node in nodes:
        weights = sorted(incoming[node], reverse=True)
        top3_sum = sum(weights[:3])
        expected_metrics[node] = top3_sum

    expected_sorted_nodes = sorted(list(nodes))

    # 2. Read the actual output file
    actual_rows = []
    with open(output_file, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) > 0, "The output file is empty."

    header = content[0].strip()
    assert header == "node_id,top3_in_weight_sum", f"Incorrect header in output file: {header}"

    actual_data = content[1:]
    assert len(actual_data) == len(expected_sorted_nodes), f"Expected {len(expected_sorted_nodes)} data rows, but found {len(actual_data)}."

    for i, row in enumerate(actual_data):
        parts = row.strip().split(',')
        assert len(parts) == 2, f"Row {i+1} is malformed: {row}"

        node_id, val_str = parts
        expected_node = expected_sorted_nodes[i]

        assert node_id == expected_node, f"Expected node '{expected_node}' at row {i+1}, but found '{node_id}'. Rows must be sorted alphabetically."

        try:
            val = int(val_str)
        except ValueError:
            pytest.fail(f"Value for node {node_id} is not an integer: {val_str}")

        expected_val = expected_metrics[node_id]
        assert val == expected_val, f"Incorrect sum for node {node_id}. Expected {expected_val}, got {val}."