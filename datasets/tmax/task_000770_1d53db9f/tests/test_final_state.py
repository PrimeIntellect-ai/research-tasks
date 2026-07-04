# test_final_state.py
import os
import pytest
import pandas as pd
import numpy as np

def test_final_output_mse():
    """
    Test that the output CSV exists and matches the golden implementation
    with an MSE <= 0.0001.
    """
    output_path = '/home/user/top_candidates.csv'
    dataset_path = '/app/data/traffic.csv'

    assert os.path.exists(output_path), f"Output file not found at {output_path}"
    assert os.path.exists(dataset_path), f"Dataset not found at {dataset_path}"

    # Generate Golden Implementation
    df = pd.read_csv(dataset_path)

    # Impute missing values
    df['impressions'] = df['impressions'].fillna(100).astype(float)
    df['clicks'] = df['clicks'].fillna(0).astype(float)

    # Compute Posterior CTR
    alpha = 12.0
    beta = 45.0
    df['posterior_ctr'] = (df['clicks'] + alpha) / (df['impressions'] + alpha + beta)

    # Compute Cosine Similarity to [1, 0, 0]
    df['similarity'] = df['emb_x']

    # Filter and Sort
    df_filtered = df[df['similarity'] >= 0.82].copy()
    df_sorted = df_filtered.sort_values(by=['posterior_ctr', 'id'], ascending=[False, True])
    golden_top = df_sorted.head(50)[['id', 'posterior_ctr', 'similarity']].reset_index(drop=True)

    # Load Agent's Output
    try:
        agent_df = pd.read_csv(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read agent's CSV output: {e}")

    assert len(agent_df) == 50, f"Expected exactly 50 rows in the output, got {len(agent_df)}"

    # Required columns
    expected_cols = ['id', 'posterior_ctr', 'similarity']
    for col in expected_cols:
        assert col in agent_df.columns, f"Missing required column '{col}' in output CSV."

    # Calculate MSE
    mse_ctr = np.mean((golden_top['posterior_ctr'] - agent_df['posterior_ctr'])**2)
    mse_sim = np.mean((golden_top['similarity'] - agent_df['similarity'])**2)

    id_matches = (golden_top['id'].values == agent_df['id'].values).sum()
    penalty = (50 - id_matches) * 1.0

    total_mse = mse_ctr + mse_sim + penalty

    threshold = 0.0001
    assert total_mse <= threshold, (
        f"Total MSE is too high. Expected <= {threshold}, got {total_mse}. "
        f"Breakdown: CTR MSE={mse_ctr}, Similarity MSE={mse_sim}, ID Penalty={penalty}"
    )