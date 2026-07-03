# test_final_state.py
import os
import pytest

def test_decoder_c_exists_and_uses_rename():
    path = "/home/user/decoder.c"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    assert "rename" in content, f"File {path} does not contain the 'rename' system call for atomic writes."

def test_processed_sample1_txt():
    path = "/home/user/processed/sample1.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "AAAAABBBCC", f"Content of {path} is incorrect. Expected 'AAAAABBBCC', got '{content}'."

def test_processed_data2_txt():
    path = "/home/user/processed/data2.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "XXXXYYYY", f"Content of {path} is incorrect. Expected 'XXXXYYYY', got '{content}'."

def test_legacy_txt_does_not_exist():
    path = "/home/user/processed/legacy.txt"
    assert not os.path.exists(path), f"File {path} should not exist because the original file was older than 7 days."

def test_processed_log():
    path = "/home/user/processed_log.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["data2.txt", "sample1.txt"]
    assert lines == expected_lines, f"Content of {path} is incorrect. Expected {expected_lines}, got {lines}."