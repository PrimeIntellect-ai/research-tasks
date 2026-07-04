# test_final_state.py

import os
import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def test_plot_validity():
    plot_path = "/home/user/cluster_plot.png"
    assert os.path.exists(plot_path), f"Plot not found at {plot_path}"
    size = os.path.getsize(plot_path)
    assert size > 15000, f"Plot is blank or too small. Expected > 15000 bytes, got {size} bytes"

def test_pca_reproducibility_metric():
    raw_path = "/home/user/raw_sensors.csv"
    reduced_path = "/home/user/reduced_data.csv"

    assert os.path.exists(raw_path), f"Raw data not found at {raw_path}"
    assert os.path.exists(reduced_path), f"Reduced data not found at {reduced_path}"

    raw_df = pd.read_csv(raw_path)
    X = raw_df.values

    # Compute canonical PCA
    scaler = StandardScaler()
    pca = PCA(n_components=2)

    X_train = X[:1000]
    scaler.fit(X_train)
    pca.fit(scaler.transform(X_train))

    expected_reduced = pca.transform(scaler.transform(X))

    # Read agent's output
    agent_reduced = pd.read_csv(reduced_path).values

    assert agent_reduced.shape == expected_reduced.shape, (
        f"Output shape mismatch. Expected {expected_reduced.shape}, got {agent_reduced.shape}"
    )

    # Check all possible PCA sign alignments
    mae_normal = np.mean(np.abs(agent_reduced - expected_reduced))
    mae_flipped_c1 = np.mean(np.abs(agent_reduced - (expected_reduced * [-1, 1])))
    mae_flipped_c2 = np.mean(np.abs(agent_reduced - (expected_reduced * [1, -1])))
    mae_flipped_both = np.mean(np.abs(agent_reduced - (expected_reduced * [-1, -1])))

    best_mae = min(mae_normal, mae_flipped_c1, mae_flipped_c2, mae_flipped_both)

    assert best_mae < 0.01, f"MAE too high: {best_mae}. Must be strictly < 0.01."