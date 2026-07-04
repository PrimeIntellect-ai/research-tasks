# test_final_state.py
import os
import json
import pytest
from sklearn.metrics import adjusted_rand_score

def test_clusters_ari():
    clusters_file = "/home/user/clusters.json"
    truth_file = "/home/user/ground_truth.json"

    assert os.path.isfile(clusters_file), f"Agent's cluster output not found at {clusters_file}."
    assert os.path.isfile(truth_file), f"Ground truth file not found at {truth_file}."

    with open(truth_file, 'r') as f:
        truth_dict = json.load(f)

    with open(clusters_file, 'r') as f:
        try:
            pred_dict = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{clusters_file} is not a valid JSON file.")

    # Reverse the agent's pred_dict (which is {cluster_id: [filenames]}) to {filename: cluster_id}
    agent_mapping = {}
    for c_id, files in pred_dict.items():
        for file in files:
            # Handle both absolute paths and basenames just in case
            agent_mapping[os.path.basename(file)] = c_id

    filenames = sorted(truth_dict.keys())

    for f in filenames:
        base_f = os.path.basename(f)
        assert base_f in agent_mapping, f"File {base_f} is missing from the agent's clusters output."

    y_true = [truth_dict[f] for f in filenames]
    y_pred = [agent_mapping[os.path.basename(f)] for f in filenames]

    ari = adjusted_rand_score(y_true, y_pred)
    assert ari >= 0.85, f"Adjusted Rand Index (ARI) is {ari:.4f}, which is below the threshold of 0.85."

def test_dendrogram_exists():
    dendrogram_file = "/home/user/dendrogram.png"
    assert os.path.isfile(dendrogram_file), f"{dendrogram_file} does not exist. Plotting script might have failed or not run."

def test_fastdtw_installed():
    try:
        import fastdtw
    except ImportError:
        pytest.fail("fastdtw package is not installed or importable. The package source might not be fixed.")