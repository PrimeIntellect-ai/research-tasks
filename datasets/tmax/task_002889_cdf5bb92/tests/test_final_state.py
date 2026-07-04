# test_final_state.py

import os
import csv

def test_correlation_plot_generated():
    plot_path = '/home/user/ml_pipeline/correlation_plot.png'
    assert os.path.isfile(plot_path), f"Expected plot file at {plot_path} is missing."

    # Check that the plot is not blank (size should be significantly larger than a blank plot)
    file_size = os.path.getsize(plot_path)
    assert file_size > 5000, f"Plot file {plot_path} is too small ({file_size} bytes), indicating it might still be blank."

def test_processed_data_csv():
    csv_path = '/home/user/ml_pipeline/processed_data.csv'
    assert os.path.isfile(csv_path), f"Expected processed data file at {csv_path} is missing."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "processed_data.csv is empty."

        # Check columns
        expected_columns = ['f1', 'f3', 'f4', 'target']
        assert header == expected_columns, f"Expected columns {expected_columns}, but got {header}. 'f2' should be dropped."

        # Check row count
        rows = list(reader)
        expected_rows = 1800
        assert len(rows) == expected_rows, f"Expected {expected_rows} rows in processed_data.csv, but got {len(rows)}."

        # Check column count for all rows
        for i, row in enumerate(rows):
            assert len(row) == 4, f"Row {i+1} has {len(row)} columns, expected 4."

def test_metrics_file():
    metrics_path = '/home/user/ml_pipeline/metrics.txt'
    assert os.path.isfile(metrics_path), f"Expected metrics file at {metrics_path} is missing."

    with open(metrics_path, 'r') as f:
        content = f.read().strip()

    assert content != "", "metrics.txt is empty."

    try:
        metric_value = float(content)
    except ValueError:
        assert False, f"metrics.txt does not contain a valid float. Found: {content}"

    assert 0.0 <= metric_value <= 1.0, f"F1 score should be between 0.0 and 1.0, but got {metric_value}."