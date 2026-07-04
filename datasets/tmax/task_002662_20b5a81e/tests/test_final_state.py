# test_final_state.py

import os
import csv
import pytest

def test_config_diff_csv():
    csv_path = "/home/user/config_diff.csv"
    assert os.path.exists(csv_path), f"The file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"The path {csv_path} is not a file."

    expected_rows = [
        ["Key", "V1_Value", "V3_Value"],
        ["app_name", "myapp", "myapp_v2"],
        ["db_host", "localhost", "db.prod"],
        ["debug", "False", "True"],
        ["port", "8080", "8081"]
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"The contents of {csv_path} do not match the expected diff. Found: {actual_rows}"

def test_skipped_files_log():
    log_path = "/home/user/skipped_files.log"
    assert os.path.exists(log_path), f"The file {log_path} does not exist."
    assert os.path.isfile(log_path), f"The path {log_path} is not a file."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_paths = [
        "../escaped_system_config.json",
        "v2/../../etc/passwd_fake"
    ]

    for path in expected_paths:
        assert path in lines, f"The malicious path '{path}' was not found in {log_path}."

def test_no_zip_slip_files():
    # Check that the malicious files were not extracted outside the target directory
    escaped_file_1 = "/home/user/escaped_system_config.json"
    escaped_file_2 = "/home/user/etc/passwd_fake"
    escaped_file_3 = "/home/user/extracted_configs/../escaped_system_config.json"
    escaped_file_4 = "/home/user/extracted_configs/v2/../../etc/passwd_fake"

    # Normalize paths to check actual locations
    check_paths = [
        os.path.normpath(escaped_file_1),
        os.path.normpath(escaped_file_2),
        os.path.normpath(escaped_file_3),
        os.path.normpath(escaped_file_4)
    ]

    for path in check_paths:
        assert not os.path.exists(path), f"Security failure: Malicious file was extracted to {path}!"

def test_extracted_configs():
    v1_config = "/home/user/extracted_configs/v1/config.json"
    v3_config = "/home/user/extracted_configs/v3/config.json"

    assert os.path.exists(v1_config), f"The file {v1_config} was not extracted."
    assert os.path.isfile(v1_config), f"The path {v1_config} is not a file."

    assert os.path.exists(v3_config), f"The file {v3_config} was not extracted."
    assert os.path.isfile(v3_config), f"The path {v3_config} is not a file."