# test_final_state.py

import os
import pytest

def test_extractor_c_exists_and_uses_mmap():
    source_path = "/home/user/extractor.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, "r") as f:
        content = f.read()

    assert "mmap" in content, f"The C source code in {source_path} does not appear to use 'mmap'."

def test_extractor_executable_exists():
    executable_path = "/home/user/extractor"
    assert os.path.isfile(executable_path), f"Executable file {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_extracted_logs_bin_content():
    output_path = "/home/user/extracted_logs.bin"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    expected_content = b"SYSTEM LOG DATA 10101010\nAUTH LOG DATA 20202020\nIMPORTANT NOTES\n"

    with open(output_path, "rb") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        f"Content of {output_path} does not match the expected extracted data. "
        f"Expected {len(expected_content)} bytes, got {len(actual_content)} bytes."
    )