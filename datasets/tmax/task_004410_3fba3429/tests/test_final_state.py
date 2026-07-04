# test_final_state.py
import os
import numpy as np
import pandas as pd
import pytest

TOLERANCE_MSE = 1e-5

def compute_ground_truth(file_path):
    edges = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                edges.append((int(parts[0]), int(parts[1])))

    if not edges:
        return [0.0] * 5

    max_node = max(max(u, v) for u, v in edges)
    n = max_node + 1
    A = np.zeros((n, n), dtype=float)
    for u, v in edges:
        A[u, v] = 1.0
        A[v, u] = 1.0

    s = np.linalg.svd(A, compute_uv=False)
    s = np.sort(s)[::-1]

    features = list(s[:5])
    while len(features) < 5:
        features.append(0.0)

    return features

def test_embeddings_csv_exists():
    agent_csv = "/home/user/embeddings.csv"
    assert os.path.exists(agent_csv), f"Output file {agent_csv} does not exist."
    assert os.path.isfile(agent_csv), f"{agent_csv} is not a file."

def test_embeddings_mse():
    dataset_dir = "/app/dataset"
    agent_csv = "/home/user/embeddings.csv"

    assert os.path.exists(agent_csv), f"Output file {agent_csv} missing."

    try:
        agent_df = pd.read_csv(agent_csv).set_index('filename')
    except Exception as e:
        pytest.fail(f"Could not read {agent_csv} as a CSV file: {e}")

    mse_list = []

    files = [f for f in os.listdir(dataset_dir) if f.endswith('.txt')]
    assert len(files) > 0, "Dataset directory is empty or missing .txt files."

    for filename in files:
        true_features = compute_ground_truth(os.path.join(dataset_dir, filename))

        assert filename in agent_df.index, f"{filename} missing from CSV."

        try:
            agent_features = agent_df.loc[filename, ['f1', 'f2', 'f3', 'f4', 'f5']].values.astype(float)
        except KeyError as e:
            pytest.fail(f"Missing expected columns in CSV for {filename}: {e}")

        mse = np.mean((np.array(true_features) - agent_features)**2)
        mse_list.append(mse)

    total_mse = np.mean(mse_list)

    assert total_mse <= TOLERANCE_MSE, f"MSE {total_mse} exceeds threshold {TOLERANCE_MSE}"