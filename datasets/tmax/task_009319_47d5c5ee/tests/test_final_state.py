# test_final_state.py

import os
import pytest

def test_phase1_authorized_keys_cleaned():
    """Verify that the authorized_keys file only contains admin@corp.local keys."""
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"File missing: {auth_keys_path}"

    with open(auth_keys_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 keys in {auth_keys_path}, found {len(lines)}"
    for line in lines:
        assert line.endswith("admin@corp.local"), f"Found a key not ending with admin@corp.local: {line}"

def test_phase1_rogue_keys_saved():
    """Verify that the rogue key was saved to rogue_keys.txt."""
    rogue_keys_path = "/home/user/rogue_keys.txt"
    assert os.path.isfile(rogue_keys_path), f"File missing: {rogue_keys_path}"

    with open(rogue_keys_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"Expected exactly 1 key in {rogue_keys_path}, found {len(lines)}"
    assert lines[0].endswith("attacker@evil.com"), f"Expected attacker key in {rogue_keys_path}, got: {lines[0]}"

def test_phase2_rogue_suid_identified():
    """Verify that the rogue SUID binary path is correctly identified."""
    rogue_suid_path = "/home/user/rogue_suid.txt"
    assert os.path.isfile(rogue_suid_path), f"File missing: {rogue_suid_path}"

    with open(rogue_suid_path, "r") as f:
        content = f.read().strip()

    expected_path = "/home/user/system_backup/kworker"
    assert content == expected_path, f"Expected '{expected_path}' in {rogue_suid_path}, got '{content}'"

def test_phase3_recovered_data():
    """Verify that the evidence was correctly decrypted and extracted."""
    recovered_file_path = "/home/user/recovered_data/project_x_intel.txt"
    assert os.path.isfile(recovered_file_path), f"File missing: {recovered_file_path}"

    with open(recovered_file_path, "r") as f:
        content = f.read().strip()

    expected_content = "CONFIDENTIAL: Project X Source Code - TOP SECRET"
    assert content == expected_content, f"Recovered data content mismatch. Expected '{expected_content}', got '{content}'"