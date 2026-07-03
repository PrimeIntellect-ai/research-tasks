# test_final_state.py

import os
import pytest

def test_detect_go_exists():
    path = "/home/user/detect.go"
    assert os.path.isfile(path), f"The Go program {path} was not created."

def test_found_archives_txt_exists():
    path = "/home/user/found_archives.txt"
    assert os.path.isfile(path), f"The output file {path} was not created."

def test_found_archives_content():
    path = "/home/user/found_archives.txt"
    assert os.path.isfile(path), f"The output file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "/home/user/project_files/hidden_gzip.dat",
        "/home/user/project_files/no_extension_file",
        "/home/user/project_files/subdir/fake_document.pdf"
    ]

    assert lines == expected, (
        f"The contents of {path} do not match the expected sorted list of archives.\n"
        f"Expected: {expected}\n"
        f"Got: {lines}"
    )