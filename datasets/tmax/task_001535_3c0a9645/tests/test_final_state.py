# test_final_state.py

import os
import pytest
import re

def test_cpp_source_exists():
    file_path = "/home/user/dedup_config.cpp"
    assert os.path.exists(file_path), f"Source file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} should be a file."

def test_executable_exists():
    file_path = "/home/user/dedup_config"
    assert os.path.exists(file_path), f"Executable file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} should be a file."
    assert os.access(file_path, os.X_OK), f"{file_path} should be executable."

def test_cleaned_configs_content():
    file_path = "/home/user/cleaned_configs.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    expected_lines = [
        "1678886400,server_port_,8080",
        "1678886401,db_hostname,db.local",
        "1678886402,feature_toggle_1,true",
        "1678886403,cache_size_mb,1024"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, f"Content of {file_path} does not match the expected final state."

def test_pipeline_log_content():
    file_path = "/home/user/pipeline.log"
    assert os.path.exists(file_path), f"Log file {file_path} is missing."

    expected_content = "Processed: 8 lines, Duplicates dropped: 4 lines"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} does not match the expected final state. Got: {content}"