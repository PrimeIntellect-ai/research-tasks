# test_final_state.py

import os
import pytest

def test_processor_files_exist():
    """Test that the C source and compiled binary exist."""
    c_file = "/home/user/processor.c"
    binary = "/home/user/processor"

    assert os.path.exists(c_file), f"C source file {c_file} is missing."
    assert os.path.exists(binary), f"Compiled binary {binary} is missing."
    assert os.access(binary, os.X_OK), f"Binary {binary} is not executable."

def test_output_csv_exists():
    """Test that the output.csv file was generated."""
    output_file = "/home/user/output.csv"
    assert os.path.exists(output_file), f"Output file {output_file} is missing."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

def test_output_csv_content():
    """Test that the output.csv file contains the correctly reshaped and gap-filled data."""
    output_file = "/home/user/output.csv"

    expected_content = (
        "Hour,Station,Temp,Status\n"
        "8,A,15.5,En_línea\n"
        "8,B,22.1,正常\n"
        "9,A,15.5,En_línea\n"
        "9,B,22.1,正常\n"
        "10,A,15.5,En_línea\n"
        "10,B,22.1,正常\n"
        "11,A,15.5,Error_🔥\n"
        "11,B,23.0,警告\n"
        "12,A,15.5,Error_🔥\n"
        "12,B,23.0,警告\n"
        "13,A,15.5,Error_🔥\n"
        "13,B,23.0,警告\n"
        "14,A,16.2,En_línea\n"
        "14,B,23.0,正常"
    )

    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == expected_content, "The content of output.csv does not match the expected reshaped and gap-filled data."