# test_final_state.py
import os
import pytest

def test_pwned_file_exists_and_content():
    pwned_file = "/home/user/audit_result/pwned.txt"
    assert os.path.isfile(pwned_file), f"File {pwned_file} does not exist. The path traversal exploit was likely unsuccessful."

    with open(pwned_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.strip() == "EXPLOITED", f"The file {pwned_file} does not contain the expected string. Found: {content!r}"