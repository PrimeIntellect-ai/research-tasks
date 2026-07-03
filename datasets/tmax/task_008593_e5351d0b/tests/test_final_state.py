# test_final_state.py

import os
import json
import pytest

def test_processed_log():
    log_file = "/home/user/processed_log.json"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {log_file} is not valid JSON.")

    expected_data = {
        "data1.csv": 110,
        "data3.xml": 350,
        "data5.json": 105
    }

    assert log_data == expected_data, f"Log file contents {log_data} do not match expected {expected_data}."

def test_incremental_backup():
    backup_dir = "/home/user/research_data/incremental_backup/"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist."

    backed_up_files = set(os.listdir(backup_dir))
    expected_files = {"data3.xml", "data5.json"}

    assert backed_up_files == expected_files, f"Backup directory contains {backed_up_files}, expected {expected_files}."

    # Verify contents match the original
    raw_dir = "/home/user/research_data/raw/"
    for filename in expected_files:
        raw_path = os.path.join(raw_dir, filename)
        backup_path = os.path.join(backup_dir, filename)

        with open(raw_path, "r") as f:
            raw_content = f.read()

        with open(backup_path, "r") as f:
            backup_content = f.read()

        assert raw_content == backup_content, f"Content of backed up file {filename} does not match the original."