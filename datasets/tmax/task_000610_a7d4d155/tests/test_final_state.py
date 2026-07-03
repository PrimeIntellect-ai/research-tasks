# test_final_state.py

import os
import subprocess
import glob
import re
import pytest

PROCESSOR_PATH = "/home/user/processor"
SCRIPT_PATH = "/home/user/process_all.sh"
CLEAN_CORPUS_DIR = "/app/data/clean"
EVIL_CORPUS_DIR = "/app/data/evil"
SERVER_DATA_DIR = "/app/server_data/data"
ACCUMULATOR_LOG = "/app/accumulator_output.log"

def is_valid_row(row):
    parts = row.strip().split(',')
    if len(parts) != 5:
        return False
    id_str, sensor_id_str, temp_str, ts_str, active_str = parts

    if not re.fullmatch(r'[0-9a-f]{8}', id_str):
        return False

    try:
        sensor_id = int(sensor_id_str)
        if not (1 <= sensor_id <= 999):
            return False
    except ValueError:
        return False

    try:
        temp = float(temp_str)
        if not (-50.0 <= temp <= 150.0):
            return False
    except ValueError:
        return False

    try:
        ts = int(ts_str)
        if not (1600000000 <= ts <= 1700000000):
            return False
    except ValueError:
        return False

    if active_str not in ("true", "false"):
        return False

    return True

def is_valid_file(filepath):
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if not lines:
                return False
            for line in lines:
                if not is_valid_row(line):
                    return False
        return True
    except Exception:
        return False

def calculate_average_temp(filepath):
    total_temp = 0.0
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 5 and parts[4] == "true":
                total_temp += float(parts[2])
                count += 1
    if count == 0:
        return 0.0
    return total_temp / count

def test_processor_exists():
    assert os.path.isfile(PROCESSOR_PATH), f"Executable {PROCESSOR_PATH} not found."
    assert os.access(PROCESSOR_PATH, os.X_OK), f"File {PROCESSOR_PATH} is not executable."

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} not found."
    assert os.access(SCRIPT_PATH, os.X_OK), f"File {SCRIPT_PATH} is not executable."

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    for f in clean_files:
        res = subprocess.run([PROCESSOR_PATH, f], capture_output=True, text=True)
        if res.returncode != 0 or "VALID" not in res.stdout:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        res = subprocess.run([PROCESSOR_PATH, f], capture_output=True, text=True)
        if res.returncode != 1 or "INVALID" not in res.stdout:
            evil_failed.append(os.path.basename(f))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_end_to_end_workflow():
    # Run the script
    res = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)

    assert os.path.isfile(ACCUMULATOR_LOG), f"Accumulator log {ACCUMULATOR_LOG} not found. Did the script run?"

    with open(ACCUMULATOR_LOG, 'r') as f:
        log_content = f.read().strip().splitlines()

    actual_results = {}
    for line in log_content:
        if ':' in line:
            fname, val = line.split(':', 1)
            actual_results[fname.strip()] = val.strip()

    # Calculate expected results
    expected_results = {}
    server_files = glob.glob(os.path.join(SERVER_DATA_DIR, "*.csv"))
    for f in server_files:
        if is_valid_file(f):
            avg = calculate_average_temp(f)
            expected_results[os.path.basename(f)] = f"{avg:.2f}"

    # Verify
    missing = []
    wrong = []
    for fname, expected_val in expected_results.items():
        if fname not in actual_results:
            missing.append(fname)
        else:
            if actual_results[fname] != expected_val:
                wrong.append(f"{fname} (expected {expected_val}, got {actual_results[fname]})")

    extra = [fname for fname in actual_results if fname not in expected_results]

    errors = []
    if missing:
        errors.append(f"Missing valid files in output: {', '.join(missing)}")
    if wrong:
        errors.append(f"Incorrect averages calculated: {', '.join(wrong)}")
    if extra:
        errors.append(f"Invalid files incorrectly processed: {', '.join(extra)}")

    if errors:
        pytest.fail(" | ".join(errors))