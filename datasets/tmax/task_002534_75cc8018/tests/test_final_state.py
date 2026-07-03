# test_final_state.py

import os
import hashlib
import re
import stat
import pytest

def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def test_output_directory_exists():
    out_dir = "/home/user/output"
    assert os.path.isdir(out_dir), f"Output directory {out_dir} does not exist."

def test_extracted_files_content():
    expected_files = {
        "intro.md": "b04be124e4d5fb737d9be70dc5d72f91",
        "setup.md": "bdd6631b518c7ed6184da3109a25d252",
        "api.md": "fd787327fc0ffdd0cf3b10b067a57ebc"
    }

    for filename, expected_md5 in expected_files.items():
        file_path = os.path.join("/home/user/output", filename)
        assert os.path.isfile(file_path), f"Extracted file {file_path} does not exist."
        actual_md5 = get_md5(file_path)
        assert actual_md5 == expected_md5, f"Content of {filename} is incorrect. Expected MD5 {expected_md5}, got {actual_md5}."

def test_extractor_c_flock():
    c_path = "/home/user/extractor.c"
    assert os.path.isfile(c_path), f"Source file {c_path} is missing."
    with open(c_path, "r") as f:
        content = f.read()

    # Check for flock usage with LOCK_EX
    assert re.search(r"flock\s*\([^,]+,\s*LOCK_EX\s*\)", content) or \
           re.search(r"flock\s*\([^,]+,\s*[^,]*LOCK_EX[^,]*\)", content) or \
           ("flock" in content and "LOCK_EX" in content), \
           "The C program does not appear to use flock() with LOCK_EX."

def test_extractor_compiled():
    bin_path = "/home/user/extractor"
    assert os.path.isfile(bin_path), f"Compiled executable {bin_path} does not exist."
    st = os.stat(bin_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File {bin_path} is not executable."