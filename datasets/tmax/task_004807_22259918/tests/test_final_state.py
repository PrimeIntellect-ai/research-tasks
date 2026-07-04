# test_final_state.py

import os
import time
import subprocess
import pytest
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

def test_pipeline_runtime_and_correctness():
    query_path = "/home/user/app/query.sql"
    edges_path = "/home/user/app/edges.csv"
    analyze_bin = "/home/user/app/analyze"
    results_path = "/home/user/results.csv"

    assert os.path.isfile(query_path), f"Missing {query_path}"
    assert os.path.isfile(analyze_bin), f"Missing executable {analyze_bin}"

    # 1. Run the SQL query to extract edges
    cmd_sql = f'psql -h localhost -U postgres -d topology -t -A -F"," -f {query_path} > {edges_path}'
    ret_sql = os.system(cmd_sql)
    assert ret_sql == 0, "Failed to execute the SQL query using psql."
    assert os.path.isfile(edges_path), f"Edges file {edges_path} was not created."

    # 2. Run the C++ analyzer and measure runtime
    start_time = time.time()
    ret_analyze = os.system(f'{analyze_bin} {edges_path}')
    end_time = time.time()

    assert ret_analyze == 0, "The C++ analyzer failed to execute successfully."

    runtime = end_time - start_time
    assert runtime < 1.5, f"Analyzer runtime was {runtime:.3f}s, which exceeds the 1.5s threshold."

    assert os.path.isfile(results_path), f"Results file {results_path} was not created."

    # 3. Read the edges and compute the reference closeness centrality
    try:
        edges_df = pd.read_csv(edges_path, header=None, names=['source', 'target'])
    except Exception as e:
        pytest.fail(f"Failed to read {edges_path}: {e}")

    if edges_df.empty:
        pytest.fail("The extracted edges.csv is empty. The SQL query might be incorrect.")

    max_node = max(edges_df['source'].max(), edges_df['target'].max())

    row = edges_df['source'].values
    col = edges_df['target'].values
    data = np.ones(len(row))

    # Create adjacency matrix
    adj = csr_matrix((data, (row, col)), shape=(max_node + 1, max_node + 1))

    # Compute all-pairs shortest paths
    dist_matrix = shortest_path(csgraph=adj, directed=True, unweighted=True)

    # Read student results
    try:
        results_df = pd.read_csv(results_path, header=None, names=['node', 'centrality'])
    except Exception as e:
        pytest.fail(f"Failed to read {results_path}: {e}")

    results_dict = dict(zip(results_df['node'], results_df['centrality']))

    # Calculate MSE
    sq_errors = []
    nodes_to_evaluate = set(edges_df['source']).union(set(edges_df['target']))

    for node in nodes_to_evaluate:
        dists = dist_matrix[node]
        reachable = dists < np.inf
        N = np.sum(reachable)

        if N <= 1:
            ref_c = 0.0
        else:
            ref_c = (N - 1) / np.sum(dists[reachable])

        student_c = results_dict.get(node, 0.0)
        sq_errors.append((student_c - ref_c) ** 2)

    mse = np.mean(sq_errors) if sq_errors else 1.0

    assert mse < 1e-5, f"MSE of centrality scores is {mse:.2e}, which exceeds the threshold of 1e-5."