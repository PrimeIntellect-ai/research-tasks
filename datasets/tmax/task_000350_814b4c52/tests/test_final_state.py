# test_final_state.py
import os
import csv
import pytest
import networkx as nx

def test_build_script_fixed():
    build_script_path = '/app/sqlite/build.sh'
    assert os.path.isfile(build_script_path), f"File {build_script_path} is missing."

    with open(build_script_path, 'r') as f:
        content = f.read()

    assert '-lpthread' in content, f"The build script {build_script_path} was not fixed to use '-lpthread'."
    assert '-lpthead' not in content, f"The build script {build_script_path} still contains the typo '-lpthead'."

def test_c_source_exists():
    c_source_path = '/home/user/shortest_path.c'
    assert os.path.isfile(c_source_path), f"The C source file {c_source_path} is missing."

def test_shortest_path_latency():
    # Re-derive the true shortest path from the CSV data
    csv_path = '/app/data/network.csv'
    assert os.path.isfile(csv_path), f"The data file {csv_path} is missing."

    G = nx.DiGraph()
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            u, v, weight = row[0], row[1], float(row[2])
            G.add_edge(u, v, weight=weight)

    try:
        true_latency = nx.shortest_path_length(G, source='NODE_START', target='NODE_END', weight='weight')
    except nx.NetworkXNoPath:
        pytest.fail("No path found in the ground truth graph, something is wrong with the setup.")

    # Read the agent's computed latency
    output_path = '/home/user/min_latency.txt'
    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    try:
        agent_latency = float(content)
    except ValueError:
        pytest.fail(f"The output file {output_path} does not contain a valid floating-point number. Found: '{content}'")

    # Calculate metric
    abs_error = abs(agent_latency - true_latency)
    threshold = 0.01

    assert abs_error <= threshold, (
        f"Absolute error {abs_error:.4f} exceeds threshold {threshold}. "
        f"Agent computed {agent_latency}, but true shortest path latency is {true_latency:.4f}."
    )