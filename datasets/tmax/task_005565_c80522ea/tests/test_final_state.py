# test_final_state.py

import os

def test_restore_success_log():
    log_path = "/home/user/restore_success.log"
    assert os.path.exists(log_path), f"Expected verification file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    expected_content = "MAILGATE_RESTORE_V1_OK\n"
    assert content == expected_content, (
        f"File {log_path} does not contain the exact expected output.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Got: {repr(content)}"
    )