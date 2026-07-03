# test_final_state.py

import os
import json
import numpy as np
import pytest

def test_annoy_setup_fixed():
    """Verify that the setup.py was fixed to use optimization flags instead of -O0."""
    setup_path = "/app/annoy-1.17.2/setup.py"
    assert os.path.isfile(setup_path), f"File {setup_path} does not exist."

    with open(setup_path, 'r') as f:
        content = f.read()

    assert "'-O0'" not in content, "The '-O0' flag is still present in setup.py, compilation will be unoptimized."
    assert "'-O3'" in content, "The '-O3' flag was not restored in setup.py."

def test_nearest_neighbors_recall():
    """Verify the nearest_neighbors.json file exists, has correct format, and achieves >= 0.95 recall."""
    results_path = "/home/user/nearest_neighbors.json"
    dataset_path = "/home/user/dataset.npy"

    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."
    assert os.path.isfile(dataset_path), f"Dataset file {dataset_path} does not exist."

    # Load exact data and normalize
    data = np.load(dataset_path)
    norms = np.linalg.norm(data, axis=1, keepdims=True)

    # Avoid division by zero
    norms[norms == 0] = 1.0
    data_normalized = data / norms

    # Load agent output
    with open(results_path, 'r') as f:
        try:
            agent_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    assert isinstance(agent_results, dict), "The JSON result must be a dictionary."

    queries = data_normalized[:100]
    # Compute exact pairwise cosine similarity (dot product on normalized)
    similarities = np.dot(queries, data_normalized.T)

    total_recall = 0.0
    for i in range(100):
        key = str(i)
        assert key in agent_results, f"Missing query index '{key}' in results."

        agent_top_10 = agent_results[key]
        assert isinstance(agent_top_10, list), f"Value for '{key}' must be a list."
        assert len(agent_top_10) == 10, f"Expected exactly 10 neighbors for query '{key}', got {len(agent_top_10)}."

        # exact top 10 (highest similarity)
        exact_top_10 = set(np.argsort(similarities[i])[-10:])
        agent_top_10_set = set(agent_top_10)

        intersection = exact_top_10.intersection(agent_top_10_set)
        total_recall += len(intersection) / 10.0

    avg_recall = total_recall / 100.0
    assert avg_recall >= 0.95, f"Recall@10 is too low: {avg_recall:.4f} (Threshold: >= 0.95)"