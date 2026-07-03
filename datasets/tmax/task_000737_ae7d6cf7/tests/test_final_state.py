# test_final_state.py

import os
import pytest

def test_phase1_patched_server():
    filepath = "/home/user/incident/patched_server.cpp"
    assert os.path.isfile(filepath), f"Phase 1 failed: {filepath} is missing."

    with open(filepath, 'r') as f:
        content = f.read()

    assert "ERROR: Invalid filename" in content, "Phase 1 failed: The patched server does not contain the exact error message 'ERROR: Invalid filename'."
    assert ".." in content or "'/'" in content or '"/"' in content, "Phase 1 failed: The patched server does not appear to check for '..' or '/'."

def test_phase2_attacker_username():
    filepath = "/home/user/incident/attacker_username.txt"
    assert os.path.isfile(filepath), f"Phase 2 failed: {filepath} is missing."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == "sys_h4x0r", f"Phase 2 failed: Expected 'sys_h4x0r', but got '{content}'."

def test_phase3_decoded_payload():
    filepath = "/home/user/incident/decoded_payload.txt"
    assert os.path.isfile(filepath), f"Phase 3 failed: {filepath} is missing."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    expected_payload = "#!/bin/bash\nrm -rf /"
    assert content == expected_payload, f"Phase 3 failed: Decoded payload does not match expected output."

def test_phase4_compromised_file():
    filepath = "/home/user/incident/compromised_file.txt"
    assert os.path.isfile(filepath), f"Phase 4 failed: {filepath} is missing."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == "ps", f"Phase 4 failed: Expected 'ps', but got '{content}'."