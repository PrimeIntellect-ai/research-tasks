# test_final_state.py

import os
import pytest

def test_extracted_directory_exists():
    """Verify that the extracted directory was created."""
    dir_path = "/home/user/extracted"
    assert os.path.isdir(dir_path), f"Expected directory {dir_path} does not exist."

def test_libmath_so_extracted_correctly():
    """Verify libmath.so was extracted and decompressed correctly."""
    file_path = "/home/user/extracted/libmath.so"
    assert os.path.isfile(file_path), f"Expected file {file_path} does not exist."

    with open(file_path, "rb") as f:
        content = f.read()

    expected_content = b"\x7FELF_MOCK_MATH_DATA_9921"
    assert content == expected_content, f"Content of {file_path} is incorrect. Expected {expected_content!r}, got {content!r}."

def test_libutils_so_extracted_correctly():
    """Verify libutils.so was extracted correctly."""
    file_path = "/home/user/extracted/libutils.so"
    assert os.path.isfile(file_path), f"Expected file {file_path} does not exist."

    with open(file_path, "rb") as f:
        content = f.read()

    expected_content = b"\x7FELF_MOCK_UTILS_DATA_4455\x00\x01\x02"
    assert content == expected_content, f"Content of {file_path} is incorrect. Expected {expected_content!r}, got {content!r}."

def test_ignored_files_not_extracted():
    """Verify that non-.so files were not extracted."""
    readme_path = "/home/user/extracted/readme.txt"
    config_path = "/home/user/extracted/config.json"

    assert not os.path.exists(readme_path), f"File {readme_path} should not have been extracted."
    assert not os.path.exists(config_path), f"File {config_path} should not have been extracted."