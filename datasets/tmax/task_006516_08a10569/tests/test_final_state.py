# test_final_state.py

import os
import re
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_pipeline.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_raw_data_synced():
    raw_dir = "/home/user/raw_data"
    staging_dir = "/opt/staging_server/data"

    assert os.path.isdir(raw_dir), f"The directory {raw_dir} does not exist."

    # Get list of csv files in staging
    staging_files = [f for f in os.listdir(staging_dir) if f.endswith('.csv')]
    raw_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]

    for f in staging_files:
        assert f in raw_files, f"File {f} was not synced to {raw_dir}."

    # Also check if sizes match
    for f in staging_files:
        staging_size = os.path.getsize(os.path.join(staging_dir, f))
        raw_size = os.path.getsize(os.path.join(raw_dir, f))
        assert staging_size == raw_size, f"File {f} in {raw_dir} does not match the size of the original file."

def test_cleaned_master_csv():
    output_path = "/home/user/cleaned_master.csv"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"The file {output_path} is empty."
    assert lines[0] == "id,name,date,country", f"The header in {output_path} is incorrect. Got: {lines[0]}"

    expected_data = [
        "101,Alice Smith,2023-05-12,US",
        "102,Charlie,2022-12-31,FR",
        "103,Bob Jones,2023-04-10,UK",
        "201,Diana,2023-01-05,DE",
        "202,Evan,2023-06-15,AU"
    ]

    actual_data = lines[1:]
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} data rows, but got {len(actual_data)}."

    for i, (expected, actual) in enumerate(zip(expected_data, actual_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected: '{expected}', Got: '{actual}'"

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    # Count how many csv files were in staging to determine expected N
    staging_dir = "/opt/staging_server/data"
    num_files = len([f for f in os.listdir(staging_dir) if f.endswith('.csv')])

    # Expected valid rows is 5 based on the setup
    num_rows = 5

    pattern1 = rf"^\[\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\] TRANSFER: Successfully synced {num_files} files\.$"
    pattern2 = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] PROCESS: Starting normalization\.$"
    pattern3 = rf"^\[\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\] COMPLETE: Processed total of {num_rows} valid rows\.$"

    assert re.search(pattern1, content, re.MULTILINE), f"Log file missing or incorrectly formatted Stage 1 message for {num_files} files."
    assert re.search(pattern2, content, re.MULTILINE), "Log file missing or incorrectly formatted Stage 2 message."
    assert re.search(pattern3, content, re.MULTILINE), f"Log file missing or incorrectly formatted Stage 3 message for {num_rows} valid rows."