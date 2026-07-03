# test_final_state.py

import os
import stat
import pytest

def test_report_builder_cpp_exists():
    file_path = "/home/user/report_builder.cpp"
    assert os.path.isfile(file_path), f"Missing required file: {file_path}"

def test_report_builder_executable_exists():
    file_path = "/home/user/report_builder"
    assert os.path.isfile(file_path), f"Missing required executable: {file_path}"
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable"

def test_process_sh_exists_and_executable():
    file_path = "/home/user/process.sh"
    assert os.path.isfile(file_path), f"Missing required script: {file_path}"
    assert os.access(file_path, os.X_OK), f"Script {file_path} is not executable"

def test_alert_log_content():
    file_path = "/home/user/alert.log"
    assert os.path.isfile(file_path), f"Missing required output file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "GATEWAY: 192.168.1.1\nWARNING_FS: /dev/sda1, /dev/sdb1, /dev/sdd1"

    assert content == expected_content, f"Content of {file_path} does not match expected output.\nExpected:\n{expected_content}\nGot:\n{content}"