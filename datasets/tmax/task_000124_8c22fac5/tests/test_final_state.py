# test_final_state.py

import os
import pytest

def test_flag_file_exists_and_correct():
    """Check that the flag.txt file exists and contains the correct flag."""
    flag_path = "/home/user/flag.txt"
    assert os.path.exists(flag_path), f"File {flag_path} is missing. Did you save the flag?"
    assert os.path.isfile(flag_path), f"Path {flag_path} is not a file."

    with open(flag_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{jWt_4lg_n0n3_byp4ss_c0nfirm3d}"
    assert content == expected_flag, f"The flag in {flag_path} is incorrect. Expected {expected_flag}, but got {content}."

def test_exploit_script_exists():
    """Check that the exploit.py script was created."""
    exploit_path = "/home/user/exploit.py"
    assert os.path.exists(exploit_path), f"File {exploit_path} is missing. Did you write the exploit script?"
    assert os.path.isfile(exploit_path), f"Path {exploit_path} is not a file."