# test_final_state.py

import os
import re

def test_processed_data_csv():
    file_path = "/home/user/remote_out/processed_data.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Did the pipeline run?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "1,alice jones,alice jones,0",
        "2,bobby,bob,2",
        "3,charlie brown,charlie brown,0",
        "4,david   smith,david smith,2"
    ]

    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in processed_data.csv, got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"

def test_crontab_entry():
    file_path = "/home/user/crontab_entry.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    # The cron expression should be for the top of every hour: 0 * * * *
    # Followed by the path to the pipeline script.
    assert content.startswith("0 * * * *"), f"Cron entry should start with '0 * * * *', got: '{content}'"
    assert "/home/user/local_process/pipeline.sh" in content, f"Cron entry should contain '/home/user/local_process/pipeline.sh', got: '{content}'"

def test_pipeline_script_exists_and_executable():
    file_path = "/home/user/local_process/pipeline.sh"
    assert os.path.isfile(file_path), f"Pipeline script {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"Pipeline script {file_path} is not executable."

def test_matcher_executable_exists():
    file_path = "/home/user/local_process/matcher"
    assert os.path.isfile(file_path), f"Compiled C++ program {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"Compiled C++ program {file_path} is not executable."