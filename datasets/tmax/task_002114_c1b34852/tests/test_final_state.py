# test_final_state.py
import os
import stat
import pytest

def test_recovered_log_exists():
    log_path = "/home/user/recovered.log"
    assert os.path.exists(log_path), f"{log_path} does not exist. Ensure your script creates this file."
    assert os.path.isfile(log_path), f"{log_path} is not a regular file."

def test_recovered_log_permissions():
    log_path = "/home/user/recovered.log"
    assert os.path.exists(log_path), f"{log_path} does not exist."

    st = os.stat(log_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Incorrect permissions on {log_path}: expected 0o600, got {oct(perms)}."

def test_recovered_log_metric():
    log_path = "/home/user/recovered.log"
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    count = content.count("EVIDENCE_CHUNK_")
    threshold = 495

    assert count >= threshold, f"recovery_count = {count}. Expected at least {threshold} recovered chunks (EVIDENCE_CHUNK_ occurrences). Check your JWT crafting and curl loop."