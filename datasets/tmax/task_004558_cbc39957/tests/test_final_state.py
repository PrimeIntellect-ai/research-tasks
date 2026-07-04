# test_final_state.py

import os
import time
import subprocess
import pandas as pd
import pytest

def get_expected_results():
    nodes_df = pd.read_csv('/home/user/graph_backup/nodes.csv', names=['node_id', 'node_type', 'timestamp', 'value'], header=0 if 'node_id' in open('/home/user/graph_backup/nodes.csv').readline() else None)
    edges_df = pd.read_csv('/home/user/graph_backup/edges.csv', names=['source_id', 'target_id', 'relationship_type'], header=0 if 'source_id' in open('/home/user/graph_backup/edges.csv').readline() else None)

    # Target nodes
    target_nodes = nodes_df[
        (nodes_df['node_type'] == 'DATABASE_SERVER') & 
        (nodes_df['timestamp'] >= 1600000000) & 
        (nodes_df['timestamp'] <= 1600086400)
    ]['node_id'].unique()

    results = {}
    for node in target_nodes:
        # Find neighbors where source is the target node and relationship is DEPENDS_ON
        neighbors_edges = edges_df[(edges_df['source_id'] == node) & (edges_df['relationship_type'] == 'DEPENDS_ON')]
        neighbor_ids = neighbors_edges['target_id'].unique()

        if len(neighbor_ids) == 0:
            continue

        neighbors = nodes_df[nodes_df['node_id'].isin(neighbor_ids)].copy()
        neighbors = neighbors.sort_values('timestamp')

        # Calculate moving average of size 3
        # Assuming the prompt implies a single value per node, we take the average of the last window
        # or if there are exactly 3 neighbors, just their average.
        if len(neighbors) >= 3:
            ma = neighbors['value'].rolling(window=3).mean().iloc[-1]
        else:
            ma = neighbors['value'].mean()

        results[str(node)] = float(ma)

    return results

def test_recovery_processor_performance_and_correctness():
    executable = "/home/user/recovery_processor"
    summary_file = "/home/user/recovery_summary.txt"

    assert os.path.isfile(executable), f"Executable not found at {executable}"

    # Measure runtime
    start = time.time()
    proc = subprocess.run([executable], capture_output=True)
    runtime = time.time() - start

    assert proc.returncode == 0, f"Program failed with return code {proc.returncode}\nStderr: {proc.stderr.decode()}"
    assert runtime <= 2.0, f"Runtime was {runtime:.2f} seconds, which exceeds the 2.0 seconds threshold."

    assert os.path.isfile(summary_file), f"Output file not found at {summary_file}"

    # Read output
    output_results = {}
    with open(summary_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 2:
                output_results[parts[0]] = float(parts[1])

    expected_results = get_expected_results()

    # Check exactness
    assert len(output_results) == len(expected_results), f"Expected {len(expected_results)} results, got {len(output_results)}"

    for node, expected_val in expected_results.items():
        assert node in output_results, f"Missing result for node {node}"
        actual_val = output_results[node]
        assert abs(actual_val - expected_val) < 1e-2, f"Incorrect moving average for node {node}: expected {expected_val}, got {actual_val}"