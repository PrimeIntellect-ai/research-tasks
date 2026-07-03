# test_final_state.py

import os
import pytest

def test_clean_metrics_exists():
    """Test that the clean_metrics.csv file exists."""
    file_path = "/home/user/clean_metrics.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing. The C program may not have run or failed to produce output."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_clean_metrics_content():
    """Test that the clean_metrics.csv file has the correct content after processing."""
    file_path = "/home/user/clean_metrics.csv"

    expected_content = (
        "1000,v1.0,45.5\n"
        "1010,v1.0,46.0\n"
        "1020,v1.0,0.0\n"
        "1030,v1.2,50.0\n"
        "1040,v1.2,52.0\n"
        "1050,v1.2,0.0\n"
        "1060,v1.2,0.0\n"
        "1070,v1.3,49.5\n"
    )

    with open(file_path, "r") as f:
        content = f.read()

    # Normalize line endings just in case
    content = content.replace("\r\n", "\n")
    if not content.endswith("\n") and content:
        content += "\n"

    assert content == expected_content, f"Content of {file_path} does not match the expected clean data. Check your C program's validation, deduplication, and gap-filling logic."

def test_processor_binary_exists():
    """Test that the compiled C program exists."""
    file_path = "/home/user/processor"
    assert os.path.exists(file_path), f"Compiled binary {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_processor_c_source_exists():
    """Test that the C source code exists."""
    file_path = "/home/user/processor.c"
    assert os.path.exists(file_path), f"C source file {file_path} is missing."