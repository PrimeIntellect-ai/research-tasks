# test_final_state.py

import os
import json
import pytest

PROJECT_DIR = "/home/user/fraud_project"
PARQUET_PATH = os.path.join(PROJECT_DIR, "data_merged.parquet")
METRICS_PATH = os.path.join(PROJECT_DIR, "metrics.json")

def test_parquet_file_exists_and_valid():
    assert os.path.isfile(PARQUET_PATH), f"Merged Parquet file is missing at {PARQUET_PATH}"

    # Check Parquet magic bytes (PAR1 at the beginning and end)
    with open(PARQUET_PATH, "rb") as f:
        header = f.read(4)
        f.seek(-4, os.SEEK_END)
        footer = f.read(4)

    assert header == b"PAR1", "File does not have a valid Parquet header."
    assert footer == b"PAR1" or footer == b"PARE", "File does not have a valid Parquet footer."

def test_metrics_json_exists_and_valid():
    assert os.path.isfile(METRICS_PATH), f"Metrics JSON file is missing at {METRICS_PATH}"

    with open(METRICS_PATH, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not a valid JSON file.")

    expected_keys = {"roc_auc_mean", "roc_auc_lower", "roc_auc_upper"}
    actual_keys = set(metrics.keys())

    assert expected_keys.issubset(actual_keys), f"metrics.json is missing required keys. Expected {expected_keys}, found {actual_keys}"

    mean_val = metrics["roc_auc_mean"]
    lower_val = metrics["roc_auc_lower"]
    upper_val = metrics["roc_auc_upper"]

    assert isinstance(mean_val, (int, float)), "roc_auc_mean must be a number"
    assert isinstance(lower_val, (int, float)), "roc_auc_lower must be a number"
    assert isinstance(upper_val, (int, float)), "roc_auc_upper must be a number"

    assert 0.0 <= mean_val <= 1.0, f"roc_auc_mean {mean_val} is out of valid ROC AUC range [0, 1]"
    assert 0.0 <= lower_val <= 1.0, f"roc_auc_lower {lower_val} is out of valid ROC AUC range [0, 1]"
    assert 0.0 <= upper_val <= 1.0, f"roc_auc_upper {upper_val} is out of valid ROC AUC range [0, 1]"

    assert lower_val <= mean_val <= upper_val, "Metrics percentiles are inconsistent: expected lower <= mean <= upper"