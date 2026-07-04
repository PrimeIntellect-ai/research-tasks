# test_final_state.py

import os
import pytest

def test_token_recovered():
    token_file = "/home/user/token.txt"
    assert os.path.isfile(token_file), f"File {token_file} does not exist. The token was not saved."

    with open(token_file, "r") as f:
        token_content = f.read().strip()

    expected_token = "SRE_MONITOR_TOK_99281aB"
    assert token_content == expected_token, f"The token in {token_file} is incorrect. Found: '{token_content}', Expected: '{expected_token}'"

def test_verification_passed():
    log_file = "/home/user/verification.log"
    assert os.path.isfile(log_file), f"File {log_file} does not exist. Did you run verify.sh?"

    with open(log_file, "r") as f:
        log_content = f.read().strip()

    expected_log = "ALL TESTS PASSED"
    assert log_content == expected_log, f"The verification log indicates failure or is incorrect. Found: '{log_content}'"