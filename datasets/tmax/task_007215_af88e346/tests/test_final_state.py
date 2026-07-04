# test_final_state.py

import os
import pytest

def test_process_go_exists():
    file_path = "/home/user/process.go"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The Go script was not created."

def test_makefile_exists():
    file_path = "/home/user/Makefile"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The Makefile was not generated."

def test_result_en():
    file_path = "/home/user/result_en.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did 'make' run successfully?"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "102", f"Expected '102' in {file_path}, but got '{content}'."

def test_result_ja():
    file_path = "/home/user/result_ja.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did 'make' run successfully?"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "202", f"Expected '202' in {file_path}, but got '{content}'."

def test_result_ar():
    file_path = "/home/user/result_ar.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did 'make' run successfully?"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "302", f"Expected '302' in {file_path}, but got '{content}'."

def test_result_ru():
    file_path = "/home/user/result_ru.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did 'make' run successfully?"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "402", f"Expected '402' in {file_path}, but got '{content}'."