# test_final_state.py

import os
import pytest

def test_recovery_log_exists():
    log_path = "/home/user/recovery.log"
    assert os.path.isfile(log_path), f"The required file {log_path} does not exist."

def test_recovery_log_content():
    log_path = "/home/user/recovery.log"
    assert os.path.isfile(log_path), f"The required file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "TXN=TXN-8849-ACBD-1102, KEY=sk_live_77a91b34f829c011x"

    assert content == expected_content, (
        f"The content of {log_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Found: '{content}'"
    )