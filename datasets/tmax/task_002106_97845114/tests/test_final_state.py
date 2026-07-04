# test_final_state.py

import os
import pandas as pd
import pytest

def test_etl_script_exists_and_executable():
    etl_script = "/home/user/etl.sh"
    assert os.path.isfile(etl_script), f"Expected ETL script not found at {etl_script}"
    assert os.access(etl_script, os.X_OK), f"ETL script {etl_script} is not executable"

def test_output_csv_exists():
    output_csv = "/home/user/total_salaries.csv"
    assert os.path.isfile(output_csv), f"Expected output CSV not found at {output_csv}"

def test_total_salaries_accuracy():
    output_csv = "/home/user/total_salaries.csv"
    truth_csv = "/app/ground_truth.csv"

    assert os.path.isfile(output_csv), "Output CSV is missing."
    assert os.path.isfile(truth_csv), "Ground truth CSV is missing."

    try:
        pred = pd.read_csv(output_csv, header=None, names=['id', 'total_salary'])
    except Exception as e:
        pytest.fail(f"Failed to read output CSV: {e}")

    try:
        truth = pd.read_csv(truth_csv, header=None, names=['id', 'total_salary'])
    except Exception as e:
        pytest.fail(f"Failed to read ground truth CSV: {e}")

    assert len(pred) == len(truth), f"Row count mismatch: expected {len(truth)}, got {len(pred)}"

    pred = pred.sort_values('id').reset_index(drop=True)
    truth = truth.sort_values('id').reset_index(drop=True)

    matches = (pred['total_salary'] == truth['total_salary']).sum()
    accuracy = matches / len(truth)

    assert accuracy >= 1.0, f"Accuracy is {accuracy:.4f}, expected >= 1.0. Some total salaries are incorrect."