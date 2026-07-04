# test_final_state.py

import os
import pandas as pd
import pytest

def evaluate_recall(truth_csv, pred_csv):
    truth = pd.read_csv(truth_csv).set_index('query_frame')
    try:
        pred = pd.read_csv(pred_csv).set_index('query_frame')
    except Exception:
        return 0.0

    correct = 0
    total = 25 # 5 queries * 5 predictions
    for q in [10, 20, 30, 40, 50]:
        if q not in pred.index:
            continue
        truth_set = set(truth.loc[q].values)
        pred_set = set(pred.loc[q].values)
        correct += len(truth_set.intersection(pred_set))

    recall = correct / total
    return recall

def test_similarities_csv_recall():
    truth_csv = "/tmp/ground_truth.csv"
    pred_csv = "/home/user/similarities.csv"

    assert os.path.exists(pred_csv), f"Output file is missing at {pred_csv}"

    score = evaluate_recall(truth_csv, pred_csv)

    assert score >= 0.8, f"Recall score {score} is below the threshold of 0.8"