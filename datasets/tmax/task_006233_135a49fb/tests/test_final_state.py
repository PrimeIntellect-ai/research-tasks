# test_final_state.py
import os
import pytest

def test_extract_c_exists():
    path = "/home/user/extract.c"
    assert os.path.isfile(path), f"Source file {path} is missing."

def test_extract_executable_exists():
    path = "/home/user/extract"
    assert os.path.isfile(path), f"Executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_docs_csv_content():
    path = "/home/user/docs.csv"
    assert os.path.isfile(path), f"Output file {path} is missing."

    expected_content = (
        "DocID,Text\n"
        "101,API Documentation Final\n"
        "102,User Guide V2 Final\n"
        "103,Internal Developer Notes\n"
        "104,Archived System Architecture\n"
    )

    with open(path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # Normalize line endings for comparison
    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]

    assert actual_lines == expected_lines, (
        f"Content of {path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )