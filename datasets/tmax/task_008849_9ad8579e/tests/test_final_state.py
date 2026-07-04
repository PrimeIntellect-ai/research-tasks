# test_final_state.py
import os
import csv
import json
import pytest

RAW_DATA_PATH = '/home/user/raw_data.csv'
PARQUET_PATH = '/home/user/processed_data.parquet'
REPORT_PATH = '/home/user/report.json'

def compute_expected_values():
    f1_vals = []
    f2_vals = []
    f3_vals = []

    with open(RAW_DATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            f1_vals.append(float(row['f1']))
            f2_vals.append(float(row['f2']))
            f3_vals.append(float(row['f3']))

    row_count = len(f1_vals)

    f1_min, f1_max = min(f1_vals), max(f1_vals)
    f2_min, f2_max = min(f2_vals), max(f2_vals)
    f3_min, f3_max = min(f3_vals), max(f3_vals)

    preds = []
    for i in range(row_count):
        f1_scaled = (f1_vals[i] - f1_min) / (f1_max - f1_min)
        f2_scaled = (f2_vals[i] - f2_min) / (f2_max - f2_min)
        f3_scaled = (f3_vals[i] - f3_min) / (f3_max - f3_min)
        pred = 0.5 * f1_scaled + 0.3 * f2_scaled - 0.2 * f3_scaled
        preds.append(pred)

    mean_pred = sum(preds) / row_count
    return row_count, round(mean_pred, 4)

def test_parquet_file_exists():
    """Test that the processed Parquet file was created."""
    assert os.path.isfile(PARQUET_PATH), f"Processed Parquet file is missing at {PARQUET_PATH}"

def test_report_json_exists():
    """Test that the report JSON file was created."""
    assert os.path.isfile(REPORT_PATH), f"Report JSON file is missing at {REPORT_PATH}"

def test_report_json_contents():
    """Test that the report JSON contains the correct keys and values."""
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    expected_row_count, expected_mean_pred = compute_expected_values()

    assert "row_count" in report, "Key 'row_count' missing from report.json"
    assert "mean_pred" in report, "Key 'mean_pred' missing from report.json"
    assert "avg_time_ms" in report, "Key 'avg_time_ms' missing from report.json"

    assert report["row_count"] == expected_row_count, f"Expected row_count to be {expected_row_count}, got {report['row_count']}"
    assert report["mean_pred"] == expected_mean_pred, f"Expected mean_pred to be {expected_mean_pred}, got {report['mean_pred']}"
    assert isinstance(report["avg_time_ms"], (int, float)), f"Expected avg_time_ms to be a number, got {type(report['avg_time_ms'])}"
    assert report["avg_time_ms"] >= 0, "Average time should be non-negative"