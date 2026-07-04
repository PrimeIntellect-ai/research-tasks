# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_results_iou():
    """
    Test that the agent's top 10 document IDs have an Intersection over Union (IoU)
    of at least 0.8 compared to the ground truth top 10 documents.
    """
    results_path = '/home/user/results.csv'
    assert os.path.isfile(results_path), f"Output file {results_path} is missing."

    docs_path = '/app/documents.csv'
    assert os.path.isfile(docs_path), f"Documents file {docs_path} is missing."

    # Read documents
    docs_df = pd.read_csv(docs_path, header=None, names=['doc_id', 'v1', 'v2', 'v3', 'v4', 'v5'])

    # Re-derive the query vector based on the transcript "find the latest financial reports"
    # and the provided vocab embeddings
    query_vec = np.array([0.4, 1.3, 1.4, 0.8, 1.0])
    query_norm = np.linalg.norm(query_vec)

    # Compute ground truth cosine similarities
    def cosine_sim(row):
        vec = np.array([row['v1'], row['v2'], row['v3'], row['v4'], row['v5']])
        vec_norm = np.linalg.norm(vec)
        if vec_norm == 0 or query_norm == 0:
            return 0.0
        return np.dot(query_vec, vec) / (query_norm * vec_norm)

    docs_df['sim'] = docs_df.apply(cosine_sim, axis=1)

    # Get ground truth top 10
    # Sorting by similarity descending. In case of ties, we preserve original order.
    truth_top_df = docs_df.sort_values(by='sim', ascending=False, kind='mergesort').head(10)
    truth_top = set(truth_top_df['doc_id'].astype(str))

    # Read agent output
    try:
        agent_df = pd.read_csv(results_path, header=None, names=['doc_id', 'score'])
        agent_top = set(agent_df['doc_id'].head(10).astype(str))
    except Exception as e:
        pytest.fail(f"Failed to read or parse {results_path}: {e}")

    # Compute IoU
    intersection = len(agent_top.intersection(truth_top))
    union = len(agent_top.union(truth_top))
    iou = intersection / union if union > 0 else 0

    # Assert metric threshold
    assert iou >= 0.8, (
        f"IoU metric failed. Computed IoU: {iou:.2f} (Threshold: >= 0.8).\n"
        f"Agent top 10: {agent_top}\n"
        f"Truth top 10: {truth_top}"
    )