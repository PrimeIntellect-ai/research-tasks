# test_final_state.py

import os
import hashlib
import pytest

def test_recover_script_exists():
    """Test that the recover.py script was created and is not empty."""
    script_path = '/home/user/forensics/recover.py'
    assert os.path.isfile(script_path), f"Script {script_path} is missing. You need to create it."
    assert os.path.getsize(script_path) > 0, f"Script {script_path} is empty."

def test_flag_file_exists_and_correct():
    """Test that the flag.txt file exists and contains the correct extracted value."""
    flag_path = '/home/user/forensics/flag.txt'
    checksum_path = '/home/user/forensics/checksum.txt'

    assert os.path.isfile(flag_path), f"Flag file {flag_path} is missing. Did your script run and produce it?"
    assert os.path.isfile(checksum_path), f"Checksum file {checksum_path} is missing."

    with open(flag_path, 'r', encoding='utf-8') as f:
        flag_content = f.read()

    with open(checksum_path, 'r', encoding='utf-8') as f:
        expected_checksum = f.read().strip()

    actual_checksum = hashlib.sha256(flag_content.encode('utf-8')).hexdigest()

    assert actual_checksum == expected_checksum, (
        f"The SHA-256 checksum of the contents in {flag_path} does not match the expected checksum in {checksum_path}. "
        "Ensure that you extracted the correct value and that there are no trailing newlines or extra spaces in your output file."
    )