# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/data_project"
PREPARE_SCRIPT = os.path.join(PROJECT_DIR, "prepare_data.sh")
PROCESSED_DATA = os.path.join(PROJECT_DIR, "processed_data.csv")
TRAIN_SCRIPT = os.path.join(PROJECT_DIR, "train_model.py")
ROC_CURVE = os.path.join(PROJECT_DIR, "roc_curve.png")
METRICS = os.path.join(PROJECT_DIR, "metrics.txt")

def test_prepare_script_exists():
    assert os.path.isfile(PREPARE_SCRIPT), f"Bash script {PREPARE_SCRIPT} is missing."
    assert os.access(PREPARE_SCRIPT, os.X_OK) or True, "prepare_data.sh should preferably be executable."

def test_processed_data_exists_and_correct():
    assert os.path.isfile(PROCESSED_DATA), f"Processed data file {PROCESSED_DATA} is missing."

    with open(PROCESSED_DATA, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 9, f"Expected 9 lines in processed_data.csv, found {len(lines)}."
    assert lines[0] == "id,feature1,feature2,target", f"Incorrect header in processed_data.csv: {lines[0]}"

    # Check that there are no empty targets
    for i, line in enumerate(lines[1:], start=2):
        parts = line.split(',')
        assert len(parts) == 4, f"Line {i} does not have exactly 4 columns: {line}"
        assert parts[3] != "", f"Line {i} has an empty target: {line}"

def test_train_model_script_modified():
    assert os.path.isfile(TRAIN_SCRIPT), f"Train script {TRAIN_SCRIPT} is missing."

    with open(TRAIN_SCRIPT, 'r') as f:
        content = f.read()

    assert "TkAgg" not in content, "train_model.py still contains the interactive 'TkAgg' backend."
    assert "Agg" in content or "pdf" in content.lower() or "svg" in content.lower(), "train_model.py does not seem to use a non-interactive backend like 'Agg'."

def test_outputs_generated():
    assert os.path.isfile(ROC_CURVE), f"ROC curve image {ROC_CURVE} is missing. Did the python script run successfully?"
    assert os.path.getsize(ROC_CURVE) > 0, f"ROC curve image {ROC_CURVE} is empty."

    assert os.path.isfile(METRICS), f"Metrics file {METRICS} is missing."
    with open(METRICS, 'r') as f:
        metrics_content = f.read()
    assert "AUC:" in metrics_content, f"Metrics file does not contain 'AUC:'. Content: {metrics_content}"