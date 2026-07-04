# test_final_state.py
import os
import json
import csv

def test_duckdb_exists():
    """Check that the DuckDB database was created."""
    db_path = '/home/user/ml_data.duckdb'
    assert os.path.exists(db_path), f"{db_path} does not exist."
    assert os.path.getsize(db_path) > 0, f"{db_path} is empty."

def test_repro_status():
    """Check that the reproducibility status is correct."""
    status_path = '/home/user/repro_status.txt'
    assert os.path.exists(status_path), f"{status_path} does not exist."
    with open(status_path, 'r') as f:
        content = f.read().strip()
    assert content == "REPRODUCIBLE", f"Expected REPRODUCIBLE in {status_path}, got {content}"

def test_predictions_csv():
    """Check the predictions CSV for correct shape and columns."""
    preds_path = '/home/user/predictions.csv'
    assert os.path.exists(preds_path), f"{preds_path} does not exist."

    with open(preds_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['id', 'class_pred', 'score_pred'], f"Incorrect columns in predictions.csv: {header}"

        row_count = sum(1 for row in reader)
        assert row_count == 1000, f"Expected 1000 prediction rows, got {row_count}"

def test_metrics_json():
    """Check the metrics JSON for correct keys and value types."""
    metrics_path = '/home/user/metrics.json'
    assert os.path.exists(metrics_path), f"{metrics_path} does not exist."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_path} is not valid JSON."

    assert 'classification_accuracy' in metrics, "Missing classification_accuracy in metrics.json"
    assert 'regression_mse' in metrics, "Missing regression_mse in metrics.json"

    assert isinstance(metrics['classification_accuracy'], (int, float)), "classification_accuracy must be a number"
    assert isinstance(metrics['regression_mse'], (int, float)), "regression_mse must be a number"