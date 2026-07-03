# test_final_state.py
import os
import pytest

def test_critical_errors_sorted_exists():
    assert os.path.isfile("/home/user/critical_errors_sorted.txt"), "The file /home/user/critical_errors_sorted.txt does not exist."

def test_critical_errors_sorted_content():
    expected_lines = [
        "CRITICAL_FAILURE: Database connection lost in app A",
        "CRITICAL_FAILURE: Disk full on node A1",
        "CRITICAL_FAILURE: Memory leak detected in B module",
        "CRITICAL_FAILURE: Process crashed in app B unexpectedly"
    ]

    with open("/home/user/critical_errors_sorted.txt", "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"Expected lines {expected_lines}, but got {actual_lines}"

def test_no_intermediate_files_extracted():
    old_logs_dir = "/home/user/old_logs"

    # The only file that should exist in /home/user/old_logs is master_archive.tar
    files_in_dir = os.listdir(old_logs_dir)
    assert "master_archive.tar" in files_in_dir, "master_archive.tar is missing from /home/user/old_logs"

    unexpected_files = [f for f in files_in_dir if f != "master_archive.tar"]
    assert not unexpected_files, f"Found unexpected extracted files in {old_logs_dir}: {unexpected_files}"

def test_python_script_exists():
    assert os.path.isfile("/home/user/process_logs.py"), "The python script /home/user/process_logs.py does not exist."