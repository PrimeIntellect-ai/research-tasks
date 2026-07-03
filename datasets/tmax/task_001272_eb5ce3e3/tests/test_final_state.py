# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_sync_events_extracted():
    output_file = "/home/user/sync_events.txt"
    assert os.path.exists(output_file), f"Output file missing: {output_file}"

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["2.50", "4.20", "8.80"]
    assert lines == expected, f"Expected timestamps {expected}, but got {lines} in {output_file}"

def test_anomaly_detector_executable():
    script_path = "/home/user/detect_anomaly.sh"
    assert os.path.exists(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/detect_anomaly.sh"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.log"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.log"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run([script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run([script_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: {', '.join(clean_failures)}")

    if errors:
        pytest.fail(" | ".join(errors))