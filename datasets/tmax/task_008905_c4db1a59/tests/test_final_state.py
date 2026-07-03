# test_final_state.py

import os
import pytest

def test_result_list_txt():
    result_file = "/home/user/result_list.txt"
    assert os.path.isfile(result_file), f"File {result_file} was not created."

    with open(result_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/processed_data/file1.utf8",
        "/home/user/processed_data/subset_A/file2.utf8"
    ]

    assert sorted(lines) == sorted(expected_lines), f"Contents of {result_file} do not match the expected output. Got: {lines}"

def test_converted_files_content():
    file1 = "/home/user/processed_data/file1.utf8"
    file2 = "/home/user/processed_data/subset_A/file2.utf8"

    assert os.path.isfile(file1), f"Converted file {file1} is missing."
    assert os.path.isfile(file2), f"Converted file {file2} is missing."

    with open(file1, "rb") as f:
        content1 = f.read()
    expected_content1 = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0xC3, 0xA9, 0x78, 0x61, 0x6D, 0x70, 0x6C, 0x65])
    assert content1 == expected_content1, f"Content of {file1} is incorrect or not properly converted to UTF-8."

    with open(file2, "rb") as f:
        content2 = f.read()
    expected_content2 = bytes([0x44, 0x61, 0x74, 0x61, 0x20, 0xC3, 0xB1, 0x6F])
    assert content2 == expected_content2, f"Content of {file2} is incorrect or not properly converted to UTF-8."

def test_no_extra_files():
    processed_dir = "/home/user/processed_data"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} is missing."

    found_files = []
    for root, _, files in os.walk(processed_dir):
        for file in files:
            found_files.append(os.path.join(root, file))

    expected_files = [
        "/home/user/processed_data/file1.utf8",
        "/home/user/processed_data/subset_A/file2.utf8"
    ]

    assert len(found_files) == len(expected_files), f"Found unexpected files in {processed_dir}. Make sure symlink loops were avoided."