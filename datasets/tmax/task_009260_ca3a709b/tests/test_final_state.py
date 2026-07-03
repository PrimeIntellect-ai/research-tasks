# test_final_state.py

import os
import csv
import pytest

def test_clean_data_csv():
    csv_path = '/home/user/clean_data.csv'
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert 'defect_count' in header, "Column 'defect_count' not found in clean_data.csv"

        idx = header.index('defect_count')
        defect_counts = []
        for row in reader:
            if len(row) > idx:
                val = row[idx]
                # Check that it's formatted as an integer (no decimal point)
                assert '.' not in val, f"Value '{val}' in defect_count is not formatted as an integer."
                defect_counts.append(val)

    expected = ['3', '1', '0', '0', '2']
    assert defect_counts == expected, f"Expected defect_count values {expected}, got {defect_counts}"

def test_mlflow_output():
    run_id_path = '/home/user/run_id.txt'
    assert os.path.exists(run_id_path), f"File {run_id_path} does not exist."

    with open(run_id_path, 'r', encoding='utf-8') as f:
        run_id = f.read().strip()

    assert run_id, "run_id.txt is empty."

    # Search for the MLflow metric file
    metric_found = False
    metric_value = None

    for root, dirs, files in os.walk('/home/user'):
        if run_id in root and 'metrics' in root:
            if 'posterior_mean_lam' in files:
                metric_found = True
                with open(os.path.join(root, 'posterior_mean_lam'), 'r') as mf:
                    content = mf.read().strip()
                    # MLflow metric files typically contain: timestamp value step
                    # e.g., "1620000000 1.15 0"
                    parts = content.split()
                    if len(parts) >= 2:
                        metric_value = float(parts[1])
                break

    assert metric_found, f"MLflow metric 'posterior_mean_lam' not found for run {run_id}."
    if metric_value is not None:
        assert 1.0 < metric_value < 1.3, f"Posterior mean {metric_value} is out of expected bounds (1.0, 1.3)."