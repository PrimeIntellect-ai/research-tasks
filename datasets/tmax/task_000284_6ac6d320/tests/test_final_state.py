# test_final_state.py
import os
import glob
import pytest

def test_extracted_files_content():
    expected_files = {
        "000000000001.bin": b"SOMEDATA_CONFIRMED_DATA12",
        "000000000002.bin": b"SOMEDATA_REJECTED_DATA",
        "000000000003.bin": b"CONFIRMED_START",
        "000000000004.bin": b"PENDING_WAITING",
        "000000000005.bin": b"ANOTHER_CONFIRMED_ITEM"
    }

    extracted_dir = "/home/user/extracted"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(extracted_dir, filename)
        assert os.path.isfile(filepath), f"Expected extracted file {filepath} is missing."

        with open(filepath, "rb") as f:
            content = f.read()

        assert content == expected_content, f"Content of {filepath} is incorrect. Expected {expected_content}, got {content}."

def test_confirmed_txt_content():
    confirmed_path = "/home/user/confirmed.txt"
    assert os.path.isfile(confirmed_path), f"File {confirmed_path} is missing."

    with open(confirmed_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "000000000001",
        "000000000003",
        "000000000005"
    ]

    assert lines == expected_lines, f"Content of {confirmed_path} is incorrect. Expected {expected_lines}, got {lines}."

def test_cpp_source_exists():
    cpp_files = glob.glob("/home/user/*.cpp")
    assert len(cpp_files) > 0, "No C++ source file (.cpp) found in /home/user/."