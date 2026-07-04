# test_final_state.py

import os
import pytest

def test_cleaned_csv_content():
    csv_path = "/home/user/cleaned.csv"
    assert os.path.isfile(csv_path), f"Expected output file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "ID,Date,Text,RollingAvgLen\n"
        "1,2023-01-01,Hello World,11.00\n"
        "2,2023-01-02,Good morning everyone,16.50\n"
        "4,2023-01-04,Yes,12.00\n"
        "6,2023-01-06,The final valid record.,15.75"
    )

    assert content == expected_content, f"The content of {csv_path} does not match the expected output."

def test_pipeline_log_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Expected log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "ERROR: Skipped invalid record.\n"
        "ERROR: Skipped invalid record."
    )

    assert content == expected_content, f"The content of {log_path} does not match the expected output."