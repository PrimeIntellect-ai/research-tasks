# test_final_state.py

import os
import stat
import re
import pytest

SECURE_LOGS_DIR = '/home/user/secure_logs'
NEW_LOG_FILE = '/home/user/secure_logs/error_summary.log'
ROTATED_LOG_FILE = '/home/user/secure_logs/error_summary.log.1'
RAW_LOG_FILE = '/home/user/raw_logs/payment.log'

def test_secure_logs_directory_permissions():
    assert os.path.exists(SECURE_LOGS_DIR), f"Directory {SECURE_LOGS_DIR} does not exist."
    mode = os.stat(SECURE_LOGS_DIR).st_mode
    perms = stat.S_IMODE(mode)
    assert perms == 0o700, f"Expected {SECURE_LOGS_DIR} to have permissions 0700, but got {oct(perms)}"

def test_rotated_log_file_permissions():
    assert os.path.exists(ROTATED_LOG_FILE), f"File {ROTATED_LOG_FILE} does not exist. Did the rotation script run?"
    mode = os.stat(ROTATED_LOG_FILE).st_mode
    perms = stat.S_IMODE(mode)
    assert perms == 0o400, f"Expected {ROTATED_LOG_FILE} to have permissions 0400, but got {oct(perms)}"

def test_new_log_file_permissions():
    assert os.path.exists(NEW_LOG_FILE), f"File {NEW_LOG_FILE} does not exist. Did the rotation script run?"
    mode = os.stat(NEW_LOG_FILE).st_mode
    perms = stat.S_IMODE(mode)
    assert perms == 0o400, f"Expected {NEW_LOG_FILE} to have permissions 0400, but got {oct(perms)}"

def test_new_log_file_is_empty():
    assert os.path.exists(NEW_LOG_FILE), f"File {NEW_LOG_FILE} does not exist."
    with open(NEW_LOG_FILE, 'r') as f:
        content = f.read()
    assert content == "", f"Expected {NEW_LOG_FILE} to be empty, but it contains data."

def test_rotated_log_file_content():
    assert os.path.exists(RAW_LOG_FILE), f"Raw log file {RAW_LOG_FILE} is missing."
    assert os.path.exists(ROTATED_LOG_FILE), f"Rotated log file {ROTATED_LOG_FILE} is missing."

    expected_lines = []
    with open(RAW_LOG_FILE, 'r') as f:
        for line in f:
            if "[ERROR]" in line and 'action="checkout"' in line:
                tx_id_match = re.search(r'tx_id="([^"]+)"', line)
                reason_match = re.search(r'reason="([^"]+)"', line)
                if tx_id_match and reason_match:
                    tx_id = tx_id_match.group(1)
                    reason = reason_match.group(1)
                    expected_lines.append(f"TX_ID: {tx_id} | REASON: {reason}")

    expected_content = "\n".join(expected_lines).strip()

    with open(ROTATED_LOG_FILE, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {ROTATED_LOG_FILE} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )