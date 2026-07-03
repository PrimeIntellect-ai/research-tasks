# test_final_state.py

import os
import pytest

def test_final_docs_exists_and_content():
    """Test that final_docs.txt exists and has the correct content."""
    final_docs_path = "/home/user/final_docs.txt"
    assert os.path.isfile(final_docs_path), f"File not found: {final_docs_path}"

    expected_content = (
        "Welcome to the system documentation.\n"
        "Chapter 1: Installation involves extracting files.\n"
        "Chapter 2: Configuration requires setting environment variables.\n"
    )

    with open(final_docs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content == expected_content, "The content of final_docs.txt does not match the expected output."

def test_decoder_exists_and_executable():
    """Test that the C source and executable exist."""
    c_source = "/home/user/decoder.c"
    executable = "/home/user/decoder"

    assert os.path.isfile(c_source), f"C source file not found: {c_source}"
    assert os.path.isfile(executable), f"Executable not found: {executable}"
    assert os.access(executable, os.X_OK), f"File is not executable: {executable}"

def test_intermediate_files_exist():
    """Test that the intermediate decoded text files exist somewhere in /home/user."""
    expected_files = ["doc_001_new.txt", "doc_002_new.txt", "doc_003_new.txt"]
    found_files = {f: False for f in expected_files}

    for root, dirs, files in os.walk("/home/user"):
        for file in files:
            if file in found_files:
                found_files[file] = True

    for f, found in found_files.items():
        assert found, f"Intermediate file {f} was not found in /home/user or its subdirectories."