# test_final_state.py

import os
import pytest

def test_c_program_exists():
    assert os.path.isfile("/home/user/smoother.c"), "The C program /home/user/smoother.c is missing."

def test_bash_script_exists():
    assert os.path.isfile("/home/user/pipeline.sh"), "The bash script /home/user/pipeline.sh is missing."

def test_clean_data_directory_and_files():
    assert os.path.isdir("/home/user/clean_data"), "The directory /home/user/clean_data/ was not created."

    expected_files = ["clean_0.csv", "clean_1.csv", "clean_2.csv", "clean_3.csv"]
    for f in expected_files:
        path = os.path.join("/home/user/clean_data", f)
        assert os.path.isfile(path), f"The cleaned file {path} was not created."

def test_final_clean_csv_content():
    final_csv_path = "/home/user/final_clean.csv"
    assert os.path.isfile(final_csv_path), f"The final merged file {final_csv_path} is missing."

    expected_lines = [
        "1,10.00",
        "2,20.00",
        "3,15.00",
        "4,30.00",
        "5,11.00",
        "6,19.00",
        "7,14.50",
        "8,29.00",
        "9,11.00",
        "10,20.00",
        "11,15.00",
        "12,30.00"
    ]

    with open(final_csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"The contents of {final_csv_path} do not match the expected sorted, smoothed output."