# test_final_state.py

import os
import sqlite3
import pandas as pd
import pytest

def test_pagerank_mse():
    db_path = '/home/user/graph.db'
    csv_path = '/home/user/pagerank_results.csv'

    assert os.path.exists(db_path), f"Database {db_path} does not exist."
    assert os.path.exists(csv_path), f"CSV results {csv_path} do not exist."

    # Connect to the original DB and fix it to get ground truth edges
    conn = sqlite3.connect(db_path)
    conn.execute("REINDEX;")

    # Extract active subgraph using recursive CTE
    query = """
    WITH RECURSIVE reachable(node) AS (
        SELECT 0
        UNION
        SELECT e.dst FROM edges e
        JOIN reachable r ON e.src = r.node
    )
    SELECT src, dst FROM edges WHERE src IN reachable AND dst IN reachable;
    """
    edges = pd.read_sql_query(query, conn)

    # Get unique nodes in subgraph
    nodes = set(edges['src']).union(set(edges['dst'])).union({0})
    N = len(nodes)

    # Compute PageRank
    pr = {n: 1.0 / N for n in nodes}
    out_degree = edges.groupby('src').size().to_dict()

    for _ in range(25):
        new_pr = {n: (1.0 - 0.85) / N for n in nodes}
        for _, row in edges.iterrows():
            u, v = row['src'], row['dst']
            new_pr[v] += 0.85 * (pr[u] / out_degree[u])
        pr = new_pr

    # Compare with agent's output
    try:
        agent_df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Could not read {csv_path} as CSV: {e}")

    assert 'node' in agent_df.columns and 'pagerank' in agent_df.columns, \
        "CSV must contain 'node' and 'pagerank' columns."

    agent_pr = dict(zip(agent_df['node'], agent_df['pagerank']))

    mse = 0.0
    for n in nodes:
        expected = pr[n]
        actual = agent_pr.get(n, 0.0)
        mse += (expected - actual) ** 2
    mse /= N

    threshold = 1e-8
    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}. The PageRank scores are incorrect."