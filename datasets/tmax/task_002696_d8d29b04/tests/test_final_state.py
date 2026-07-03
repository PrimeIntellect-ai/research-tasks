# test_final_state.py

import os
import pytest

def test_found_backup_txt():
    filepath = "/home/user/found_backup.txt"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == "service_77.bin", f"Expected 'service_77.bin' in {filepath}, but found '{content}'."

def test_exploit_bin():
    filepath = "/home/user/exploit.bin"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    expected_pt = b'{"user":"attacker","role":"system_root"}'
    key = b"\xde\xad\xbe\xef"
    expected_ct = bytes([expected_pt[i] ^ key[i % 4] for i in range(len(expected_pt))])

    with open(filepath, "rb") as f:
        actual_ct = f.read()

    assert actual_ct == expected_ct, f"The contents of {filepath} do not match the expected ciphertext."