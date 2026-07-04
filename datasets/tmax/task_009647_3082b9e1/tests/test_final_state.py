# test_final_state.py

import os
import csv
from collections import defaultdict
import pytest

def test_script_exists():
    script_path = '/home/user/extract_subgraph.sh'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_cypher_output():
    output_path = '/home/user/subgraph.cypher'
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    # Recompute the expected subgraph based on the actual CSV files
    nodes = {}
    nodes_csv = '/home/user/data/nodes.csv'
    edges_csv = '/home/user/data/edges.csv'

    assert os.path.isfile(nodes_csv), f"Missing {nodes_csv}"
    assert os.path.isfile(edges_csv), f"Missing {edges_csv}"

    with open(nodes_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[row['node_id']] = row

    edges = []
    adj = defaultdict(set)
    with open(edges_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            edges.append(row)
            adj[row['src_id']].add(row['dst_id'])
            adj[row['dst_id']].add(row['src_id'])

    # Traversal logic
    target = 'U-007'
    hop0 = {target}

    hop1 = set()
    for n in hop0:
        hop1.update(adj[n])

    hop2 = set()
    for n in hop1:
        hop2.update(adj[n])

    valid_nodes = hop0 | hop1 | hop2

    # Filter edges
    valid_edges = [e for e in edges if e['src_id'] in valid_nodes and e['dst_id'] in valid_nodes]

    expected_lines = []

    # Format nodes
    sorted_nodes = sorted([n for n in valid_nodes if n in nodes])
    for n in sorted_nodes:
        node = nodes[n]
        expected_lines.append(f"CREATE (:{node['label']} {{id: '{node['node_id']}', name: '{node['name']}'}});")

    expected_lines.append("")

    # Format edges
    sorted_edges = sorted(valid_edges, key=lambda x: (x['src_id'], x['dst_id']))
    for e in sorted_edges:
        expected_lines.append(f"MATCH (a {{id: '{e['src_id']}'}}), (b {{id: '{e['dst_id']}'}}) CREATE (a)-[:{e['relation']} {{weight: {e['weight']}}}]->(b);")

    expected_content = "\n".join(expected_lines).strip()

    # Read the actual output
    with open(output_path, 'r') as f:
        actual_lines = f.read().strip().splitlines()

    # Strip trailing whitespaces from actual lines
    actual_content = "\n".join(line.rstrip() for line in actual_lines).strip()

    assert actual_content == expected_content, (
        f"The content of {output_path} does not match the expected Cypher format or subgraph logic.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )