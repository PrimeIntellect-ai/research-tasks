# test_final_state.py
import os
import pytest

SPOOL_DIR = "/home/user/storage_spool"
REPORT_FILE = "/home/user/text_size_report.txt"

def test_renamed_binary_files():
    # Check that binary files were renamed with .bak
    expected_bak_files = [
        "data_02.dat.bak",
        "data_04.dat.bak"
    ]
    for file_name in expected_bak_files:
        file_path = os.path.join(SPOOL_DIR, file_name)
        assert os.path.isfile(file_path), f"Expected binary file to be renamed to {file_path}, but it was not found."

def test_unchanged_text_files():
    # Check that text files were NOT renamed
    expected_text_files = [
        "data_01.dat",
        "data_03.dat",
        "data_05.dat"
    ]
    for file_name in expected_text_files:
        file_path = os.path.join(SPOOL_DIR, file_name)
        assert os.path.isfile(file_path), f"Expected text file {file_path} to remain unchanged, but it was not found."

def test_original_binary_files_removed():
    # Check that original binary files no longer exist
    unexpected_files = [
        "data_02.dat",
        "data_04.dat"
    ]
    for file_name in unexpected_files:
        file_path = os.path.join(SPOOL_DIR, file_name)
        assert not os.path.exists(file_path), f"Original binary file {file_path} should have been renamed, but it still exists."

def test_report_file_content():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."
    with open(REPORT_FILE, "r") as f:
        content = f.read().strip()

    assert content == "53", f"Expected report file content to be '53', but got '{content}'."