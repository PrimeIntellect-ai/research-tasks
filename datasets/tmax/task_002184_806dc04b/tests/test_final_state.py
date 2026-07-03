# test_final_state.py
import json
import math
import subprocess
import sqlite3
import io
import os
import pytest
import pandas as pd
import networkx as nx

def test_top_nodes_json_exists():
    path = "/home/user/top_nodes.json"
    assert os.path.exists(path), f"Output file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_pagerank_rmse():
    path = "/home/user/top_nodes.json"
    assert os.path.exists(path), f"Output file {path} does not exist."

    # Generate reference
    proc = subprocess.run(['/app/legacy_pathfinder', '99'], stdout=subprocess.PIPE, text=True, check=True)
    edges = pd.read_csv(io.StringIO(proc.stdout))

    db_path = '/home/user/backup_meta.db'
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    nodes = pd.read_sql_query('SELECT * FROM nodes', conn)
    conn.close()

    # Join logic
    merged = edges.merge(nodes, left_on='source_node_id', right_on='node_id', suffixes=('', '_src'))
    merged = merged.merge(nodes, left_on='target_node_id', right_on='node_id', suffixes=('_src', '_tgt'))

    valid_edges = merged[
        (merged['region_src'] == merged['region_tgt']) | 
        (merged['is_global_src'] == 1)
    ]

    G = nx.from_pandas_edgelist(valid_edges, 'source_node_id', 'target_node_id', create_using=nx.DiGraph())
    pr = nx.pagerank(G, alpha=0.85)
    sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)[:50]
    reference_dict = {k: v for k, v in sorted_pr}

    # Read agent output
    with open(path, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert isinstance(agent_data, list), "JSON output must be a list of objects."
    assert len(agent_data) == 50, f"Expected exactly 50 nodes, found {len(agent_data)}."

    agent_dict = {}
    for i, item in enumerate(agent_data):
        assert 'node_id' in item, f"Item at index {i} missing 'node_id'."
        assert 'pagerank' in item, f"Item at index {i} missing 'pagerank'."
        agent_dict[item['node_id']] = item['pagerank']

    # Compute RMSE
    sq_errors = []
    for node_id, ref_val in reference_dict.items():
        agent_val = agent_dict.get(node_id, 0.0)
        sq_errors.append((ref_val - agent_val) ** 2)

    rmse = math.sqrt(sum(sq_errors) / len(sq_errors))

    threshold = 0.0001
    assert rmse <= threshold, f"RMSE {rmse} is greater than the threshold {threshold}."