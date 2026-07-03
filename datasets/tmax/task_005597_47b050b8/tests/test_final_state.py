# test_final_state.py

import os
import pytest

def test_c_source_exists():
    assert os.path.isfile("/home/user/incident/investigate.c"), "The C source file /home/user/incident/investigate.c does not exist."

def test_compiled_binary_exists():
    assert os.path.isfile("/home/user/incident/investigate"), "The compiled binary /home/user/incident/investigate does not exist. Did you compile it?"
    assert os.access("/home/user/incident/investigate", os.X_OK), "The file /home/user/incident/investigate is not executable."

def test_redacted_payload_exists():
    assert os.path.isfile("/home/user/incident/redacted_payload.txt"), "The output file /home/user/incident/redacted_payload.txt does not exist."

def test_redacted_payload_content():
    expected_content = '{"username":"sysadmin","session_id":"98765","ssn":"***-**-****","role":"root"}'

    with open("/home/user/incident/redacted_payload.txt", "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"The redacted payload content is incorrect.\nExpected: '{expected_content}'\nGot: '{actual_content}'"