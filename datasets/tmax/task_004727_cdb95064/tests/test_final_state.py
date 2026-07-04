# test_final_state.py

import os
import pytest

def test_extracted_files_exist():
    expected_files = [
        "/home/user/extracted/test1.txt",
        "/home/user/extracted/test2.txt",
        "/home/user/extracted/test3.txt"
    ]
    for file_path in expected_files:
        assert os.path.exists(file_path), f"Extracted file {file_path} is missing."
        assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_extracted_file_contents():
    # test1.txt
    with open("/home/user/extracted/test1.txt", "rb") as f:
        content = f.read()
    assert content == b"AAAAABBBBBCCCCCDDDDD", "test1.txt content is incorrect."

    # test2.txt
    expected_text2 = "Café au lait and piña coladas are müy bien! " * 5
    with open("/home/user/extracted/test2.txt", "rb") as f:
        content = f.read()
    assert content == expected_text2.encode("utf-8"), "test2.txt content or encoding is incorrect."

    # test3.txt
    expected_text3 = "ñ" * 100 + "A" * 50 + "é" * 100
    with open("/home/user/extracted/test3.txt", "rb") as f:
        content = f.read()
    assert content == expected_text3.encode("utf-8"), "test3.txt content or encoding is incorrect."

def test_extraction_log():
    log_path = "/home/user/extraction_log.txt"
    assert os.path.exists(log_path), f"Log file {log_path} is missing."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "test1.txt successfully extracted. Final UTF-8 size: 20 bytes",
        "test2.txt successfully extracted. Final UTF-8 size: 235 bytes",
        "test3.txt successfully extracted. Final UTF-8 size: 450 bytes"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in log file, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Log file line {i+1} mismatch. Expected: '{expected}', Actual: '{actual}'"