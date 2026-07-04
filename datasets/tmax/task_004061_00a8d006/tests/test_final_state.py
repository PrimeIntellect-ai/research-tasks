# test_final_state.py
import os
import pandas as pd
from sklearn.metrics import roc_auc_score
import pytest

def test_anomaly_scores_csv():
    csv_path = '/home/user/anomaly_scores.csv'
    assert os.path.exists(csv_path), f"Error: {csv_path} not found."

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to parse CSV file: {e}")

    assert 'frame_id' in df.columns, "Error: CSV must contain 'frame_id' column."
    assert 'score' in df.columns, "Error: CSV must contain 'score' column."

    df = df.sort_values('frame_id')
    y_scores = df['score'].values

    assert len(y_scores) == 200, f"Error: Expected 200 scores, got {len(y_scores)}"

    gt_path = '/app/ground_truth.txt'
    assert os.path.exists(gt_path), f"Error: {gt_path} not found."

    with open(gt_path, 'r') as f:
        y_true = [int(x.strip()) for x in f.readlines()]

    assert len(y_true) == 200, f"Error: Expected 200 ground truth labels, got {len(y_true)}"

    try:
        auc = roc_auc_score(y_true, y_scores)
    except Exception as e:
        pytest.fail(f"Failed to calculate ROC AUC score: {e}")

    assert auc >= 0.90, f"Failure: AUC below threshold. Expected >= 0.90, got {auc:.4f}"