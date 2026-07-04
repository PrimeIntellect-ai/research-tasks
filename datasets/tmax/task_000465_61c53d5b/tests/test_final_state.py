# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_BIN = "/home/user/detector"
SANCTIONED_TXT = "/home/user/sanctioned.txt"
CLEAN_DIR = "/app/clean"
EVIL_DIR = "/app/evil"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_BIN), f"Detector binary not found at {DETECTOR_BIN}"
    assert os.access(DETECTOR_BIN, os.X_OK), f"Detector binary at {DETECTOR_BIN} is not executable"

def test_sanctioned_txt_exists():
    assert os.path.isfile(SANCTIONED_TXT), f"Sanctioned text file not found at {SANCTIONED_TXT}"

def test_adversarial_corpus():
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]

    assert len(evil_files) > 0, "No evil CSV files found."
    assert len(clean_files) > 0, "No clean CSV files found."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        try:
            result = subprocess.run(
                [DETECTOR_BIN, evil_file, SANCTIONED_TXT],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "EVIL":
                evil_bypassed.append((os.path.basename(evil_file), output))
        except Exception as e:
            evil_bypassed.append((os.path.basename(evil_file), str(e)))

    for clean_file in clean_files:
        try:
            result = subprocess.run(
                [DETECTOR_BIN, clean_file, SANCTIONED_TXT],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_modified.append((os.path.basename(clean_file), output))
        except Exception as e:
            clean_modified.append((os.path.basename(clean_file), str(e)))

    error_msgs = []
    if evil_bypassed:
        bypassed_names = [f[0] for f in evil_bypassed]
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {bypassed_names}")
    if clean_modified:
        modified_names = [f[0] for f in clean_modified]
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (flagged as EVIL or failed): {modified_names}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))