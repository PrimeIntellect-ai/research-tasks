# test_final_state.py

import os
import pandas as pd
from sklearn.metrics import adjusted_rand_score

def test_artifact_phases_csv():
    csv_path = '/home/user/artifact_phases.csv'

    # Check if the file exists
    assert os.path.exists(csv_path), f"Output file not found at {csv_path}"
    assert os.path.isfile(csv_path), f"Path {csv_path} is not a file"

    # Read the CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        assert False, f"Failed to read {csv_path} as a CSV file: {e}"

    # Check columns
    expected_columns = ['frame_index', 'phase_cluster']
    for col in expected_columns:
        assert col in df.columns, f"Missing required column '{col}' in {csv_path}"

    # Check row count
    assert len(df) == 60, f"Expected exactly 60 rows in {csv_path}, but found {len(df)}"

    # Sort by frame_index to ensure chronological order
    df = df.sort_values('frame_index')

    # Ground truth: 3 distinct phases of 20 frames each
    true_labels = [0]*20 + [1]*20 + [2]*20
    pred_labels = df['phase_cluster'].tolist()

    # Calculate Adjusted Rand Index (ARI)
    ari = adjusted_rand_score(true_labels, pred_labels)

    # Assert against the threshold
    threshold = 0.85
    assert ari >= threshold, f"Adjusted Rand Index (ARI) is {ari:.4f}, which is below the threshold of {threshold}"