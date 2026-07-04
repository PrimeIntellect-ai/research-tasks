# test_final_state.py

import os
import pytest

def test_organized_data_files():
    organized_dir = "/home/user/organized_data"
    assert os.path.isdir(organized_dir), f"Directory {organized_dir} is missing."

    expected_files = {
        "file1.txt": "hello",
        "file2.txt": "café",
        "file4.txt": "jalapeño"
    }

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(organized_dir, filename)
        assert os.path.isfile(filepath), f"Expected processed file {filepath} is missing."

        with open(filepath, "rb") as f:
            content = f.read()
            # Decode as utf-8, strip trailing newlines if any
            try:
                text_content = content.decode("utf-8").strip()
            except UnicodeDecodeError:
                pytest.fail(f"File {filepath} is not valid UTF-8.")

            assert text_content == expected_content, f"Content of {filepath} is incorrect. Expected '{expected_content}', got '{text_content}'."

def test_ignored_file():
    filepath = "/home/user/organized_data/file3.txt"
    assert not os.path.exists(filepath), f"File {filepath} should not exist because it fails the magic check."

def test_processed_log():
    log_path = "/home/user/processed.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["file1.txt", "file2.txt", "file4.txt"]
    assert lines == expected_lines, f"Contents of {log_path} are incorrect or not sorted. Expected {expected_lines}, got {lines}."