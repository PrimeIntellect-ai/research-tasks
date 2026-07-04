# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    file_path = "/home/user/dedup.c"
    assert os.path.isfile(file_path), f"The C source file {file_path} is missing."

def test_cleaned_products_file_exists():
    file_path = "/home/user/cleaned_products.txt"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

def test_cleaned_products_content():
    file_path = "/home/user/cleaned_products.txt"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

    expected_lines = [
        "apple iphone 14",
        "samsung galaxy s23",
        "google pixel 7",
        "sony xperia 1",
        "oneplus 11"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip("\n") for line in f.readlines()]

    # Strip any trailing empty lines if present
    while actual_lines and actual_lines[-1] == "":
        actual_lines.pop()

    assert actual_lines == expected_lines, f"The contents of {file_path} do not match the expected deduplicated output."