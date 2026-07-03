# test_final_state.py

import os
import pytest

def test_admin_execute_stats_exists():
    """Check that /home/user/admin_execute_stats.tsv exists."""
    path = "/home/user/admin_execute_stats.tsv"
    assert os.path.isfile(path), f"Missing output file: {path}"

def test_admin_execute_stats_content():
    """Compute the expected output from nodes and edges and verify the output file."""
    nodes_path = "/home/user/nodes.tsv"
    edges_path = "/home/user/edges.tsv"
    output_path = "/home/user/admin_execute_stats.tsv"

    # Read nodes
    admin_nodes = {}
    with open(nodes_path, 'r') as f:
        for line in f:
            parts = line.strip('\n').split('\t')
            if len(parts) >= 3:
                node_id, entity_name, role = parts[0], parts[1], parts[2]
                if role == 'Admin':
                    admin_nodes[node_id] = entity_name

    # Read edges and count
    execute_counts = {node_id: 0 for node_id in admin_nodes}
    with open(edges_path, 'r') as f:
        for line in f:
            parts = line.strip('\n').split('\t')
            if len(parts) >= 3:
                source_id, target_id, action_type = parts[0], parts[1], parts[2]
                if source_id in admin_nodes and action_type == 'Execute':
                    execute_counts[source_id] += 1

    # Prepare expected output
    results = []
    for node_id, count in execute_counts.items():
        if count > 0:
            results.append((admin_nodes[node_id], count))

    # Sort: count descending, then entity_name ascending
    results.sort(key=lambda x: (-x[1], x[0]))

    expected_lines = [f"{entity}\t{count}" for entity, count in results]

    # Read actual output
    with open(output_path, 'r') as f:
        actual_lines = [line.strip('\n') for line in f if line.strip('\n')]

    assert actual_lines == expected_lines, (
        f"Output file {output_path} content does not match expected.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )