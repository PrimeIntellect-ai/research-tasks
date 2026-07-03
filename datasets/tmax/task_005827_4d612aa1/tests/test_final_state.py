# test_final_state.py

import os
import pytest

def test_docs_extracted():
    extracted_file = "/home/user/docs/draft_logs.txt"
    assert os.path.isfile(extracted_file), f"{extracted_file} does not exist. Archive was not extracted correctly."

def test_parsed_logs_csv():
    csv_path = "/home/user/parsed_logs.csv"
    assert os.path.isfile(csv_path), f"{csv_path} does not exist."

    expected_csv = (
        "Alice,API_Reference,Draft\n"
        "Bob,User_Guide,Review\n"
        "Charlie,Release_Notes,Final\n"
    )

    with open(csv_path, "r") as f:
        content = f.read().strip() + "\n"

    assert content == expected_csv, "The contents of parsed_logs.csv do not match the expected output."

def test_processor_cpp_locking():
    cpp_path = "/home/user/processor.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    has_headers = "<sys/file.h>" in content or "<fcntl.h>" in content
    assert has_headers, "processor.cpp does not include <sys/file.h> or <fcntl.h> for file locking."

    has_locking = "flock(" in content or "F_SETLK" in content or "F_SETLKW" in content
    assert has_locking, "processor.cpp does not seem to use flock or fcntl for file locking."

def test_registry_txt():
    txt_path = "/home/user/registry.txt"
    assert os.path.isfile(txt_path), f"{txt_path} does not exist."

    expected_txt = (
        "[Draft] API_Reference updated by Alice\n"
        "[Review] User_Guide updated by Bob\n"
        "[Final] Release_Notes updated by Charlie\n"
    )

    with open(txt_path, "r") as f:
        content = f.read().strip() + "\n"

    assert content == expected_txt, "The contents of registry.txt do not match the expected output."

def test_registry_bin():
    bin_path = "/home/user/registry.bin"
    assert os.path.isfile(bin_path), f"{bin_path} does not exist."

    expected_bin = b"API_Reference\0User_Guide\0Release_Notes\0"

    with open(bin_path, "rb") as f:
        content = f.read()

    assert content == expected_bin, "The contents of registry.bin do not match the expected binary output."