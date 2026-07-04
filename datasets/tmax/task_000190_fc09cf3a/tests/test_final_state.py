# test_final_state.py

import os
import pytest

def test_key_found():
    key_file = "/home/user/key_found.txt"
    assert os.path.exists(key_file), f"The file {key_file} does not exist."
    assert os.path.isfile(key_file), f"{key_file} is not a file."

    with open(key_file, "r") as f:
        content = f.read()

    assert "XorEvasionKey99!" in content, f"The extracted key was not found in {key_file}."

def test_forge_c_exists():
    forge_file = "/home/user/forge.c"
    assert os.path.exists(forge_file), f"The file {forge_file} does not exist."
    assert os.path.isfile(forge_file), f"{forge_file} is not a file."

def test_payload_bin_size():
    payload_file = "/home/user/payload.bin"
    assert os.path.exists(payload_file), f"The file {payload_file} does not exist."
    assert os.path.isfile(payload_file), f"{payload_file} is not a file."

    size = os.path.getsize(payload_file)
    assert size == 32, f"The payload file {payload_file} is {size} bytes long, but must be exactly 32 bytes."

def test_success_log():
    log_file = "/home/user/success.log"
    assert os.path.exists(log_file), f"The file {log_file} does not exist. The payload may not have been executed successfully."
    assert os.path.isfile(log_file), f"{log_file} is not a file."

    with open(log_file, "r") as f:
        content = f.read()

    assert "sysadmin logged in" in content, f"The success log {log_file} does not contain the expected success message."