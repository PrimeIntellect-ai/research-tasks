# test_final_state.py

import os
import json
import sqlite3
import pytest
import math

def test_output_file_exists():
    output_path = '/home/user/output_graph_metrics.json'
    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

def test_output_json_structure_and_values():
    output_path = '/home/user/output_graph_metrics.json'
    assert os.path.isfile(output_path), "Output file missing."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    assert "metadata" in data, "Missing 'metadata' in output JSON."
    assert "top_nodes" in data, "Missing 'top_nodes' in output JSON."

    # Check metadata
    metadata = data["metadata"]
    assert metadata.get("threshold") == 50.0, "Incorrect threshold in metadata."
    assert metadata.get("date_start") == "2023-01-01", "Incorrect date_start in metadata."
    assert metadata.get("date_end") == "2023-01-31", "Incorrect date_end in metadata."

    # Recompute graph from database to verify PageRank
    db_path = '/home/user/transactions.db'
    assert os.path.isfile(db_path), "Database file missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sender, receiver, amount 
        FROM transactions 
        WHERE amount > 50.0 AND tx_date BETWEEN '2023-01-01' AND '2023-01-31'
    ''')
    rows = cursor.fetchall()
    conn.close()

    # Build graph
    edges = {}
    nodes = set()
    for sender, receiver, amount in rows:
        nodes.add(sender)
        nodes.add(receiver)
        if sender not in edges:
            edges[sender] = {}
        edges[sender][receiver] = edges[sender].get(receiver, 0.0) + amount

    # Python implementation of PageRank to match NetworkX (alpha=0.85, weight='weight')
    N = len(nodes)
    pr = {n: 1.0 / N for n in nodes}
    alpha = 0.85

    # Power iteration
    for _ in range(100):
        new_pr = {n: 0.0 for n in nodes}
        dangling_sum = sum(pr[n] for n in nodes if n not in edges or not edges[n])

        for n in nodes:
            # Base teleportation + dangling node redistribution
            new_pr[n] += (1.0 - alpha) / N + alpha * dangling_sum / N

        for n in nodes:
            if n in edges and edges[n]:
                total_weight = sum(edges[n].values())
                for out_n, weight in edges[n].items():
                    new_pr[out_n] += alpha * pr[n] * (weight / total_weight)

        # Check convergence (optional, 100 iterations is enough for this small graph)
        pr = new_pr

    sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    expected_top_3 = sorted_pr[:3]

    top_nodes = data["top_nodes"]
    assert isinstance(top_nodes, list), "'top_nodes' should be a list."
    assert len(top_nodes) == 3, f"Expected 3 top nodes, found {len(top_nodes)}."

    for i, expected in enumerate(expected_top_3):
        exp_acc, exp_score = expected
        act_acc = top_nodes[i].get("account")
        act_score = top_nodes[i].get("pagerank")

        assert act_acc == exp_acc, f"Rank {i+1} account mismatch: expected {exp_acc}, got {act_acc}."
        assert act_score is not None, f"Rank {i+1} missing 'pagerank'."
        assert math.isclose(act_score, exp_score, rel_tol=1e-3, abs_tol=1e-3), \
            f"Rank {i+1} pagerank mismatch for {exp_acc}: expected ~{exp_score:.4f}, got {act_score}."