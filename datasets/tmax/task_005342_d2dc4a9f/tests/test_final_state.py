# test_final_state.py

import os
import numpy as np
import pandas as pd
import pytest

def test_pagerank_mse():
    # 1. Compute Ground Truth using numpy to avoid reliance on unlisted packages
    edges = [
        ("Alice", "Bob", 2),
        ("Bob", "Charlie", 3),
        ("Alice", "Dave", 1),
        ("Dave", "Charlie", 2),
        ("Charlie", "Alice", 4), # from audio
        ("Dave", "Eve", 2),      # from audio
        ("Eve", "Charlie", 5)    # from audio
    ]

    # Aggregate edges just like the evaluator
    edge_weights = {}
    for u, v, w in edges:
        if (u, v) in edge_weights:
            edge_weights[(u, v)] += w
        else:
            edge_weights[(u, v)] = w

    nodes = list(set([u for u, v in edge_weights.keys()] + [v for u, v in edge_weights.keys()]))
    nodes.sort()
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)

    # Adjacency matrix
    A = np.zeros((n, n))
    for (u, v), w in edge_weights.items():
        A[node_to_idx[u], node_to_idx[v]] = w

    # Out-degree sums
    out_sums = A.sum(axis=1)

    # Transition matrix
    M = np.zeros((n, n))
    for i in range(n):
        if out_sums[i] > 0:
            M[i, :] = A[i, :] / out_sums[i]
        else:
            M[i, :] = 1.0 / n

    # PageRank power iteration
    alpha = 0.85
    pr = np.ones(n) / n
    for _ in range(100):
        pr = alpha * np.dot(M.T, pr) + (1 - alpha) / n

    truth_pr = {nodes[i]: pr[i] for i in range(n)}

    # 2. Read Agent's Output
    agent_file = "/home/user/pagerank_results.csv"
    assert os.path.exists(agent_file), f"Agent's output file not found at {agent_file}"

    try:
        df_agent = pd.read_csv(agent_file)
        assert 'node' in df_agent.columns and 'pagerank_score' in df_agent.columns, \
            "CSV must contain 'node' and 'pagerank_score' columns"
        agent_pr = dict(zip(df_agent['node'], df_agent['pagerank_score']))
    except Exception as e:
        pytest.fail(f"Could not read or parse agent's output file: {e}")

    # 3. Calculate MSE
    mse_sum = 0.0
    all_nodes = set(truth_pr.keys()).union(set(agent_pr.keys()))
    for node in all_nodes:
        t_val = truth_pr.get(node, 0.0)
        try:
            a_val = float(agent_pr.get(node, 0.0))
        except ValueError:
            a_val = 0.0
        mse_sum += (t_val - a_val) ** 2

    mse = mse_sum / max(len(all_nodes), 1)

    # 4. Assert against threshold
    threshold = 0.00001
    assert mse < threshold, f"MSE {mse:.8f} is not strictly less than {threshold}"