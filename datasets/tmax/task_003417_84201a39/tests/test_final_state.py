# test_final_state.py

import os
import hashlib

def test_success_txt_contains_pin():
    success_file = "/home/user/success.txt"
    assert os.path.exists(success_file), f"{success_file} does not exist. Did the trigger script execute correctly?"

    with open(success_file, "r") as f:
        content = f.read().strip()

    assert content == "7492", f"Expected {success_file} to contain the cracked PIN '7492', but found '{content}'."

def test_trigger_py_exists_and_bypasses_filter():
    trigger_file = "/home/user/sandbox/trigger.py"
    assert os.path.exists(trigger_file), f"{trigger_file} does not exist. The payload was not uploaded to the correct location."

    with open(trigger_file, "rb") as f:
        header = f.read(10)

    assert b"GIF" in header, f"The first 10 bytes of {trigger_file} do not contain 'GIF'. The upload filter bypass was not implemented correctly."

def test_payload_hash_matches():
    trigger_file = "/home/user/sandbox/trigger.py"
    hash_file = "/home/user/payload_hash.txt"

    assert os.path.exists(trigger_file), f"{trigger_file} missing, cannot verify hash."
    assert os.path.exists(hash_file), f"{hash_file} does not exist. The exploit script did not write the payload hash."

    with open(trigger_file, "rb") as f:
        trigger_content = f.read()

    expected_hash = hashlib.sha256(trigger_content).hexdigest()

    with open(hash_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The hash in {hash_file} ({actual_hash}) does not match the actual SHA-256 hash of {trigger_file} ({expected_hash})."

def test_exploit_script_exists():
    exploit_file = "/home/user/exploit.py"
    assert os.path.exists(exploit_file), f"The exploit script {exploit_file} is missing."