# test_final_state.py

import os
import pytest

def test_extracted_files_txt():
    txt_path = "/home/user/extracted_files.txt"
    assert os.path.isfile(txt_path), f"File does not exist: {txt_path}"

    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "/home/user/project/main.py",
        "/home/user/project/utils/helper.py"
    ]

    assert lines == expected, f"Content of {txt_path} does not match expected output. Got: {lines}"

def test_extracted_files_content():
    main_path = "/home/user/project/main.py"
    helper_path = "/home/user/project/utils/helper.py"

    assert os.path.isfile(main_path), f"File does not exist: {main_path}"
    with open(main_path, 'rb') as f:
        assert f.read() == b'print("Hello World")', f"Incorrect content in {main_path}"

    assert os.path.isfile(helper_path), f"File does not exist: {helper_path}"
    with open(helper_path, 'rb') as f:
        assert f.read() == b'def help(): pass', f"Incorrect content in {helper_path}"

def test_malicious_files_skipped():
    secret_leak_path = "/home/user/secret_leak.txt"
    overwrite_path = "/home/user/data/overwrite.txt"

    assert not os.path.exists(secret_leak_path), f"Malicious file was extracted: {secret_leak_path}"

    # We should also ensure overwrite.txt is not created, but wait - the setup script writes the backup.json to /home/user/data/backup.json.
    # We just need to check overwrite.txt doesn't exist.
    assert not os.path.exists(overwrite_path), f"Malicious file was extracted: {overwrite_path}"