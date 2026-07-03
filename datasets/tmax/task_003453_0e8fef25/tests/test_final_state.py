# test_final_state.py

import os
import numpy as np
import pytest
from PIL import Image

def test_queries_fixed_metric():
    queries_fixed_path = '/home/user/queries_fixed.npy'
    embeddings_path = '/home/user/embeddings.npy'
    ground_truth_path = '/home/user/ground_truth.npy'

    assert os.path.exists(queries_fixed_path), f"File {queries_fixed_path} is missing."
    assert os.path.exists(embeddings_path), f"File {embeddings_path} is missing."
    assert os.path.exists(ground_truth_path), f"File {ground_truth_path} is missing."

    queries_all = np.load(queries_fixed_path)
    assert queries_all.shape == (100, 50), f"Expected queries_fixed to have shape (100, 50), got {queries_all.shape}."

    queries = queries_all[20:]
    embeddings = np.load(embeddings_path)
    ground_truth = np.load(ground_truth_path)[20:]

    # Recompute Recall@10
    dist = np.sum(queries**2, axis=1)[:, np.newaxis] + np.sum(embeddings**2, axis=1) - 2 * np.dot(queries, embeddings.T)
    top_k = np.argsort(dist, axis=1)[:, :10]

    hits = [1 if gt in top_k[i] else 0 for i, gt in enumerate(ground_truth)]
    recall = np.mean(hits)

    threshold = 0.85
    assert recall >= threshold, f"Expected Recall@10 >= {threshold}, but got {recall:.4f}"

def test_plot_generated():
    plot_path = '/home/user/recall_plot.png'
    assert os.path.exists(plot_path), f"Plot file {plot_path} is missing."

    try:
        with Image.open(plot_path) as img:
            img.verify()
    except Exception as e:
        pytest.fail(f"Plot file {plot_path} is not a valid image. Error: {e}")

def test_metrics_code_fixed():
    metrics_path = '/app/custom_vec_eval-1.0.0/custom_vec_eval/metrics.py'
    assert os.path.exists(metrics_path), f"File {metrics_path} is missing."

    with open(metrics_path, 'r') as f:
        content = f.read()

    assert "- 2 * np.dot" in content or "-2 * np.dot" in content or "-2*np.dot" in content or "- 2*np.dot" in content, \
        "The distance formula in metrics.py does not appear to be corrected (should use - 2 * np.dot)."

def test_plot_code_fixed():
    plot_code_path = '/app/custom_vec_eval-1.0.0/custom_vec_eval/plot.py'
    assert os.path.exists(plot_code_path), f"File {plot_code_path} is missing."

    with open(plot_code_path, 'r') as f:
        content = f.read()

    assert "matplotlib.use('Template')" not in content, \
        "The matplotlib backend in plot.py is still set to 'Template'."