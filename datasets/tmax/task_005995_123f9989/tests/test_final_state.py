# test_final_state.py

import os
import re
import pytest

RAW_LOGS_PATH = "/home/user/raw_logs.txt"
CSV_PATH = "/home/user/import_ready.csv"
PIPELINE_LOG_PATH = "/home/user/pipeline.log"
C_SOURCE_PATH = "/home/user/process_logs.c"
C_BIN_PATH = "/home/user/process_logs"

def test_c_files_exist():
    assert os.path.exists(C_SOURCE_PATH), f"C source file missing: {C_SOURCE_PATH}"
    assert os.path.isfile(C_SOURCE_PATH), f"Not a file: {C_SOURCE_PATH}"

    assert os.path.exists(C_BIN_PATH), f"Compiled binary missing: {C_BIN_PATH}"
    assert os.path.isfile(C_BIN_PATH), f"Not a file: {C_BIN_PATH}"
    assert os.access(C_BIN_PATH, os.X_OK), f"Binary is not executable: {C_BIN_PATH}"

def test_csv_output():
    assert os.path.exists(CSV_PATH), f"CSV output file missing: {CSV_PATH}"
    assert os.path.isfile(CSV_PATH), f"Not a file: {CSV_PATH}"

    # Derive expected rows from the raw logs
    assert os.path.exists(RAW_LOGS_PATH), f"Raw logs missing, cannot verify: {RAW_LOGS_PATH}"

    expected_rows = []
    counts = {'2': 0, '4': 0, '5': 0}

    pattern = re.compile(r'^\[(.*?)\] \[(.*?)\] \[(.*?)\] \[(.*?)\]$')

    with open(RAW_LOGS_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                timestamp, ip, status, msg = match.groups()
                category = status[0]
                if category in counts and counts[category] < 5:
                    counts[category] += 1
                    expected_rows.append(f"{timestamp},{ip},{status},{msg}")

            if all(c == 5 for c in counts.values()):
                break

    expected_csv_content = ["timestamp,ip_address,status_code,message"] + expected_rows

    with open(CSV_PATH, "r") as f:
        actual_csv_content = [line.strip() for line in f if line.strip()]

    assert actual_csv_content == expected_csv_content, (
        f"CSV content in {CSV_PATH} does not match the expected stratified sample.\n"
        f"Expected {len(expected_csv_content)} rows, got {len(actual_csv_content)} rows."
    )

def test_pipeline_log_summary():
    assert os.path.exists(PIPELINE_LOG_PATH), f"Pipeline log missing: {PIPELINE_LOG_PATH}"
    assert os.path.isfile(PIPELINE_LOG_PATH), f"Not a file: {PIPELINE_LOG_PATH}"

    # We expect 5 of each based on the raw logs provided
    expected_log_entry = "[PROCESS_LOG] Stratification complete: 5 2xx, 5 4xx, 5 5xx extracted."

    with open(PIPELINE_LOG_PATH, "r") as f:
        log_content = f.read()

    assert expected_log_entry in log_content, (
        f"Expected summary log entry not found in {PIPELINE_LOG_PATH}.\n"
        f"Expected to find: '{expected_log_entry}'"
    )