# test_final_state.py

import os
import json
import subprocess
import glob
import pytest
import csv

def test_video_joined_csv():
    joined_path = "/home/user/video_joined.csv"
    assert os.path.exists(joined_path), f"File not found: {joined_path}"

    with open(joined_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 50, f"Expected 50 rows in {joined_path}, found {len(rows)}"

    # Check timestamp 2.5
    row_25 = next((r for r in rows if abs(float(r['timestamp']) - 2.5) < 0.01), None)
    assert row_25 is not None, "Row with timestamp 2.5 not found"

    brightness = float(row_25['brightness'])
    assert abs(brightness - 245.0) < 5.0, f"Expected brightness near 245.0 at timestamp 2.5, got {brightness}"

    assert row_25['speed'] != '', "Speed at timestamp 2.5 should not be empty"
    assert row_25['speed'].lower() != 'nan', "Speed at timestamp 2.5 should not be NaN"

def test_experiment_log():
    log_path = "/home/user/experiment_log.json"
    assert os.path.exists(log_path), f"File not found: {log_path}"

    with open(log_path, 'r') as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {log_path} is not valid JSON")

    assert log_data.get("video_frames_processed") == 50, "Expected video_frames_processed to be 50"
    assert abs(log_data.get("max_brightness", 0) - 245.0) < 5.0, "Expected max_brightness near 245.0"
    assert log_data.get("missing_speeds_imputed") == 2, "Expected missing_speeds_imputed to be 2"

def test_adversarial_detector():
    detector_path = "/home/user/detector"
    assert os.path.exists(detector_path), f"Detector binary not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector binary at {detector_path} is not executable"

    clean_files = glob.glob("/app/hidden_corpus/clean/*.csv")
    evil_files = glob.glob("/app/hidden_corpus/evil/*.csv")

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run([detector_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run([detector_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))