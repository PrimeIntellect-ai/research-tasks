# test_final_state.py
import os
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
import pytest

def test_annoy_installed():
    try:
        import annoy
    except ImportError:
        pytest.fail("The 'annoy' library is not installed or failed to import. Did you fix setup.py and install it?")

def test_metric_recall_at_10():
    bootstrapped_path = '/home/user/bootstrapped_data.csv'
    neighbors_path = '/home/user/neighbors.csv'
    embeddings_path = '/home/user/embeddings.csv'

    assert os.path.exists(bootstrapped_path), f"File not found: {bootstrapped_path}"
    assert os.path.exists(neighbors_path), f"File not found: {neighbors_path}"
    assert os.path.exists(embeddings_path), f"File not found: {embeddings_path}"

    # 1. Reproduce the exact cleaned baseline data
    raw_data = pd.read_csv(embeddings_path, header=None).values
    col_means = np.nanmean(raw_data, axis=0)
    nan_inds = np.where(np.isnan(raw_data))
    raw_data[nan_inds] = col_means[nan_inds[1]]
    cleaned_data = np.clip(raw_data, -2.0, 2.0)

    # 2. Load agent's bootstrapped data and neighbor predictions
    bootstrapped_data = pd.read_csv(bootstrapped_path, header=None).values
    agent_neighbors = pd.read_csv(neighbors_path, header=None).values

    assert bootstrapped_data.shape == (5000, 50), f"Bootstrapped data shape is incorrect: {bootstrapped_data.shape}, expected (5000, 50)"
    assert agent_neighbors.shape == (100, 10), f"Neighbors file shape is incorrect: {agent_neighbors.shape}, expected (100, 10)"

    # 3. Compute exact brute-force nearest neighbors
    query_data = cleaned_data[:100]
    distances = cdist(query_data, bootstrapped_data, metric='euclidean')

    recall_scores = []
    for i in range(100):
        # exact top 10
        exact_top_10 = set(np.argsort(distances[i])[:10])
        # agent top 10
        agent_top_10 = set(agent_neighbors[i])

        overlap = len(exact_top_10.intersection(agent_top_10))
        recall_scores.append(overlap / 10.0)

    mean_recall = np.mean(recall_scores)

    assert mean_recall >= 0.95, f"Metric failed: Recall@10 is {mean_recall:.4f}, expected >= 0.95"