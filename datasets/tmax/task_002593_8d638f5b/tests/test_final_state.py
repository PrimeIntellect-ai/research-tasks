# test_final_state.py

import os
import csv
import re
import math
import pytest

DATASET_PATH = "/home/user/pipeline/data/dataset.csv"
OUTPUT_CSV_PATH = "/home/user/pipeline/output/normalized.csv"
METRICS_LOG_PATH = "/home/user/pipeline/output/metrics.log"
EXECUTABLE_PATH = "/home/user/pipeline/build/normalize_tool"
SCRIPT_PATH = "/home/user/pipeline/run_experiment.sh"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}. Did you build the tool?"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File at {EXECUTABLE_PATH} is not executable."

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable."

def test_metrics_log():
    assert os.path.isfile(METRICS_LOG_PATH), f"Metrics log not found at {METRICS_LOG_PATH}. Did you redirect stdout?"

    # Compute expected min/max from dataset
    assert os.path.isfile(DATASET_PATH), f"Dataset not found at {DATASET_PATH}."
    train_vals = []
    with open(DATASET_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['is_train']) == 1:
                train_vals.append(float(row['feature_1']))

    expected_min = min(train_vals)
    expected_max = max(train_vals)

    with open(METRICS_LOG_PATH, 'r') as f:
        log_content = f.read().strip()

    # Expecting format: "Feature 1: min=<val>, max=<val>"
    match = re.search(r"Feature 1:\s*min=([0-9\.\-]+),\s*max=([0-9\.\-]+)", log_content)
    assert match is not None, f"Could not parse metrics log. Content was: {log_content}"

    actual_min = float(match.group(1))
    actual_max = float(match.group(2))

    assert math.isclose(actual_min, expected_min, rel_tol=1e-5), f"Expected min={expected_min}, but got {actual_min}"
    assert math.isclose(actual_max, expected_max, rel_tol=1e-5), f"Expected max={expected_max}, but got {actual_max}"

def test_normalized_csv():
    assert os.path.isfile(OUTPUT_CSV_PATH), f"Output CSV not found at {OUTPUT_CSV_PATH}."

    # Compute expected scaled values
    assert os.path.isfile(DATASET_PATH), f"Dataset not found at {DATASET_PATH}."
    train_vals = []
    rows = []
    with open(DATASET_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            if int(row['is_train']) == 1:
                train_vals.append(float(row['feature_1']))

    expected_min = min(train_vals)
    expected_max = max(train_vals)

    expected_scaled = {}
    for row in rows:
        val = float(row['feature_1'])
        scaled = (val - expected_min) / (expected_max - expected_min)
        expected_scaled[row['id']] = scaled

    with open(OUTPUT_CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        assert 'feature_1_scaled' in reader.fieldnames, "Output CSV missing 'feature_1_scaled' column."

        for row in reader:
            row_id = row['id']
            actual_scaled = float(row['feature_1_scaled'])
            assert row_id in expected_scaled, f"Unexpected id {row_id} in output CSV."
            expected_val = expected_scaled[row_id]
            assert math.isclose(actual_scaled, expected_val, abs_tol=1e-4), \
                f"Row id={row_id}: expected scaled value {expected_val:.4f}, but got {actual_scaled:.4f}"