# test_final_state.py

import os
import pandas as pd
import pytest

def test_report_accuracy():
    report_path = "/home/user/report.csv"
    truth_path = "/tmp/ground_truth.csv"

    assert os.path.exists(report_path), f"Report file not found at {report_path}"
    assert os.path.isfile(report_path), f"{report_path} is not a file"
    assert os.path.exists(truth_path), f"Ground truth file not found at {truth_path}"

    try:
        pred = pd.read_csv(report_path)
    except Exception as e:
        pytest.fail(f"Failed to read {report_path} as CSV: {e}")

    try:
        truth = pd.read_csv(truth_path)
    except Exception as e:
        pytest.fail(f"Failed to read {truth_path} as CSV: {e}")

    assert 'filename' in pred.columns, f"'filename' column missing in {report_path}"
    assert 'is_malicious' in pred.columns, f"'is_malicious' column missing in {report_path}"

    merged = pd.merge(truth, pred, on='filename', suffixes=('_truth', '_pred'))

    assert len(merged) > 0, "No matching filenames found between the report and ground truth"

    correct = (merged['is_malicious_truth'] == merged['is_malicious_pred']).sum()
    accuracy = correct / len(truth)

    threshold = 0.95
    assert accuracy >= threshold, f"Accuracy {accuracy:.4f} is below the required threshold of {threshold}"