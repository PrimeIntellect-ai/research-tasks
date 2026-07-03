# test_final_state.py

import os
import pytest

def test_validator_source_exists():
    assert os.path.isfile("/home/user/validator.c"), "The C source file /home/user/validator.c is missing."

def test_validator_executable_exists():
    assert os.path.isfile("/home/user/validator"), "The compiled executable /home/user/validator is missing."
    assert os.access("/home/user/validator", os.X_OK), "The file /home/user/validator is not executable."

def test_corrupted_files_txt():
    output_file = "/home/user/corrupted_files.txt"
    assert os.path.isfile(output_file), f"The output file {output_file} is missing."

    expected_files = [
        "/home/user/storage_pool/dir_a/corrupt_magic.bin",
        "/home/user/storage_pool/dir_b/short_payload.bak",
        "/home/user/storage_pool/dir_b/sub_c/trunc_header.dat",
        "/home/user/storage_pool/long_payload.archive"
    ]
    expected_files.sort()

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_files, f"The contents of {output_file} do not match the expected sorted list of corrupted files."