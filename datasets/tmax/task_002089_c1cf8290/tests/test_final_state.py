# test_final_state.py
import os
import csv
import math
import subprocess
import pytest

def test_video_telemetry_extraction():
    csv_path = '/home/user/video_telemetry.csv'
    assert os.path.isfile(csv_path), f"Telemetry CSV file {csv_path} is missing."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['frame_index', 'brightness'], f"CSV header is incorrect. Expected ['frame_index', 'brightness'], got {header}."

        rows = list(reader)
        assert len(rows) == 100, f"Expected 100 rows of telemetry data, got {len(rows)}."

        for i, row in enumerate(rows):
            assert len(row) == 2, f"Row {i} has incorrect number of columns."
            frame_index = int(row[0])
            brightness = float(row[1])

            assert frame_index == i, f"Expected frame_index {i}, got {frame_index}."

            expected_brightness = 100 + 50 * math.sin(i * 0.1)
            assert abs(brightness - expected_brightness) <= 1.0, f"Row {i}: Expected brightness ~{expected_brightness:.2f}, got {brightness}."

def test_adversarial_classifier():
    classifier_path = '/home/user/classifier.py'
    assert os.path.isfile(classifier_path), f"Classifier script {classifier_path} is missing."

    clean_dir = '/app/corpus/test/clean'
    evil_dir = '/app/corpus/test/evil'

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean test files found."
    assert len(evil_files) > 0, "No evil test files found."

    clean_failures = []
    for fpath in clean_files:
        result = subprocess.run(['python3', classifier_path, fpath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != 'CLEAN':
            clean_failures.append((os.path.basename(fpath), output))

    evil_failures = []
    for fpath in evil_files:
        result = subprocess.run(['python3', classifier_path, fpath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != 'EVIL':
            evil_failures.append((os.path.basename(fpath), output))

    error_msg = ""
    if clean_failures:
        error_msg += f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected. Offending files: {[f[0] for f in clean_failures]}.\n"
    if evil_failures:
        error_msg += f"{len(evil_failures)} of {len(evil_files)} evil bypassed. Offending files: {[f[0] for f in evil_failures]}.\n"

    assert not clean_failures and not evil_failures, error_msg.strip()