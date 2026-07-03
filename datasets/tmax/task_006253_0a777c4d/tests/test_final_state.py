# test_final_state.py

import os
import pytest

def test_final_docs_01():
    """Verify the contents of the first merged document."""
    file_path = "/home/user/final_docs/01_Introduction_To_System.md"
    assert os.path.isfile(file_path), f"Missing merged document: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "Welcome to the system.\n"
        "This is the first paragraph.\n"
        "This is the second part of the introduction."
    )

    assert content == expected_content, f"Content of {file_path} does not match expected output."

def test_final_docs_02():
    """Verify the contents of the second merged document."""
    file_path = "/home/user/final_docs/02_API_Reference.md"
    assert os.path.isfile(file_path), f"Missing merged document: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "The API has the following endpoints:\n"
        "- /v1/auth\n"
        "- /v1/data"
    )

    assert content == expected_content, f"Content of {file_path} does not match expected output."

def test_chapter_index_log():
    """Verify the chapter index log exists and contains correct mappings."""
    log_path = "/home/user/chapter_index.log"
    assert os.path.isfile(log_path), f"Missing log file: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert "Chap_01:Introduction_To_System" in lines, f"Missing Chap_01 mapping in {log_path}"
    assert "Chap_02:API_Reference" in lines, f"Missing Chap_02 mapping in {log_path}"

def test_c_parser_exists():
    """Verify the C parser source and executable exist."""
    src_path = "/home/user/parser.c"
    bin_path = "/home/user/parser"

    assert os.path.isfile(src_path), f"Missing C source file: {src_path}"
    assert os.path.isfile(bin_path), f"Missing compiled executable: {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Compiled parser is not executable: {bin_path}"

def test_scripts_exist():
    """Verify the Bash scripts exist."""
    step1 = "/home/user/step1_extract.sh"
    step3 = "/home/user/step3_build.sh"

    assert os.path.isfile(step1), f"Missing extraction script: {step1}"
    assert os.path.isfile(step3), f"Missing build script: {step3}"