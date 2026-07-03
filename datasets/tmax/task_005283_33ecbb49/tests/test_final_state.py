# test_final_state.py

import os
import json
import numpy as np
import pytest

def test_benchmark_results_exist():
    results_path = "/home/user/benchmark_results.json"
    assert os.path.exists(results_path), f"Output file {results_path} does not exist. Did you run the benchmark script?"
    assert os.path.isfile(results_path), f"{results_path} is not a file."

def test_benchmark_performance_and_correctness():
    results_path = "/home/user/benchmark_results.json"
    assert os.path.exists(results_path), f"Output file {results_path} is missing."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON from {results_path}")

    assert "inference_time_seconds" in results, "Missing 'inference_time_seconds' in results JSON"
    assert "top_5_indices" in results, "Missing 'top_5_indices' in results JSON"

    time_taken = results['inference_time_seconds']
    assert isinstance(time_taken, (int, float)), "inference_time_seconds must be a number"

    # Check performance metric
    threshold = 0.25
    assert time_taken < threshold, (
        f"Inference too slow: {time_taken}s (threshold {threshold}s). "
        "Did you fix the C-extension optimization flags in setup.py and reinstall the package?"
    )

    # Check correctness
    try:
        refs = np.vstack([np.load(f'/home/user/data/ref_chunk_{i}.npy') for i in range(10)])
        queries = np.load('/home/user/data/queries.npy')
        pca = np.load('/home/user/data/pca_matrix.npy')
    except Exception as e:
        pytest.fail(f"Failed to load data files for verification: {e}")

    # Projection
    proj_refs = refs @ pca.T
    proj_queries = queries @ pca.T

    # Exact L2 distance squared
    dists = np.sum(proj_queries**2, axis=1, keepdims=True) + np.sum(proj_refs**2, axis=1) - 2 * np.dot(proj_queries, proj_refs.T)
    expected_indices = np.argsort(dists, axis=1)[:, :5].tolist()

    agent_indices = results['top_5_indices']

    assert len(agent_indices) == len(expected_indices), (
        f"Expected {len(expected_indices)} query results, got {len(agent_indices)}"
    )

    assert np.array_equal(agent_indices, expected_indices), (
        "Top 5 indices do not match the ground truth PCA projection and KNN logic."
    )