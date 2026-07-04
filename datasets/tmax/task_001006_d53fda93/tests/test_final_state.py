# test_final_state.py

import os
import subprocess
import pytest

DETECT_SCRIPT = "/home/user/detect.sh"
PIPELINE_BIN = "/home/user/pipeline"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_detect_script_exists_and_executable():
    assert os.path.isfile(DETECT_SCRIPT), f"{DETECT_SCRIPT} does not exist."
    assert os.access(DETECT_SCRIPT, os.X_OK), f"{DETECT_SCRIPT} is not executable."

def test_pipeline_exists_and_executable():
    assert os.path.isfile(PIPELINE_BIN), f"{PIPELINE_BIN} does not exist."
    assert os.access(PIPELINE_BIN, os.X_OK), f"{PIPELINE_BIN} is not executable."

def test_detector_adversarial_corpus():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]

    clean_failures = []
    evil_failures = []

    for cf in clean_files:
        result = subprocess.run([DETECT_SCRIPT, cf], capture_output=True, text=True)
        if result.stdout.strip() != "CLEAN":
            clean_failures.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([DETECT_SCRIPT, ef], capture_output=True, text=True)
        if result.stdout.strip() != "EVIL":
            evil_failures.append(os.path.basename(ef))

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (failed to classify as CLEAN): {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (failed to classify as EVIL): {', '.join(evil_failures)}")

    assert not clean_failures and not evil_failures, " | ".join(error_msg)

def test_pipeline_functionality():
    input_data = """1620000000,sensor_A,10.0
1620000000,sensor_A,10.0
1620000010,sensor_A,20.0
1620000060,sensor_A,30.0
1620000120,sensor_A,40.0
1620000180,sensor_A,50.0
1620000000,sensor_B,-5.0
1620000000,sensor_C,9999.0
"""
    # Deduplication: 1st row kept, 2nd row dropped.
    # Bucket 1620000000: sensor_A avg = (10+20)/2 = 15.0
    # Bucket 1620000060: sensor_A avg = 30.0. Moving avg (window 3) = (15.0 + 30.0)/2 = 22.5
    # Bucket 1620000120: sensor_A avg = 40.0. Moving avg (window 3) = (15.0 + 30.0 + 40.0)/3 = 28.333
    # Bucket 1620000180: sensor_A avg = 50.0. Moving avg (window 3) = (30.0 + 40.0 + 50.0)/3 = 40.0

    result = subprocess.run([PIPELINE_BIN], input=input_data, capture_output=True, text=True)
    assert result.returncode == 0, "Pipeline failed to execute"

    output_lines = result.stdout.strip().split('\n')

    # Check that evil rows are filtered
    assert not any("sensor_B" in line for line in output_lines), "Pipeline failed to filter negative values"
    assert not any("sensor_C" in line for line in output_lines), "Pipeline failed to filter high values"

    # Check deduplication and moving averages
    assert "1620000000,sensor_A,15" in output_lines[0] or "1620000000,sensor_A,15.0" in output_lines[0]
    assert "1620000060,sensor_A,22.5" in output_lines[1]
    assert "1620000120,sensor_A,28.3" in output_lines[2]
    assert "1620000180,sensor_A,40" in output_lines[3] or "1620000180,sensor_A,40.0" in output_lines[3]