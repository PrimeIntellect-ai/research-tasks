# test_final_state.py

import os
import pytest

def test_flag_txt_content():
    flag_path = "/home/user/recovery/flag.txt"
    assert os.path.isfile(flag_path), f"File {flag_path} does not exist. Did you extract the flag?"

    with open(flag_path, "rb") as f:
        content = f.read()

    expected_flag = b"FLAG{w4l_p4rs3}"
    assert content == expected_flag, f"Content of {flag_path} is incorrect. Expected {expected_flag!r}, got {content!r}"

def test_zip_slip_fix():
    malicious_path_outside = "/home/user/malicious.txt"
    assert not os.path.exists(malicious_path_outside), f"File {malicious_path_outside} exists. The Zip Slip vulnerability was not properly fixed."

def test_extracted_files():
    malicious_path_inside = "/home/user/recovery/malicious.txt"
    wal_path = "/home/user/recovery/database.wal"

    assert os.path.isfile(malicious_path_inside), f"File {malicious_path_inside} does not exist. The malicious file was not extracted to the recovery directory using its base name."
    assert os.path.isfile(wal_path), f"File {wal_path} does not exist. The database.wal file was not extracted."