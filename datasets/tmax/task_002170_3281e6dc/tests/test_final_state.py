# test_final_state.py

import os
import re
import pytest

def test_auth_key_exists_and_correct():
    auth_key_path = "/tmp/auth.key"
    assert os.path.isfile(auth_key_path), f"The file {auth_key_path} does not exist."
    with open(auth_key_path, "r") as f:
        content = f.read().strip()
    assert content == "auth_secret_998877abc", f"The auth key content is incorrect. Found: {content}"

def test_parser_c_fixed():
    parser_path = "/home/user/log_processor/parser.c"
    assert os.path.isfile(parser_path), f"The file {parser_path} does not exist."
    with open(parser_path, "r") as f:
        content = f.read()

    # Check that sscanf return value is checked (e.g., == 3)
    assert re.search(r"sscanf\s*\(.*?\)\s*==\s*3", content) or re.search(r"3\s*==\s*sscanf\s*\(.*?\)", content) or re.search(r"sscanf\s*\(.*?\)\s*!=\s*3", content), "parser.c does not check if sscanf successfully parsed 3 integers."

    # Check that assert is present
    assert re.search(r"assert\s*\(.*?!=?\s*0\s*\)", content) or re.search(r"assert\s*\(.*?\)", content), "parser.c does not contain an assert statement for the divisor."

    # Check that it skips when the third integer is 0
    assert "continue" in content or "if" in content, "parser.c does not seem to have logic to skip malformed or zero-divisor lines."

def test_final_result():
    result_path = "/home/user/final_result.txt"
    assert os.path.isfile(result_path), f"The file {result_path} does not exist."
    with open(result_path, "r") as f:
        content = f.read().strip()
    assert content == "Total: 61", f"The final result is incorrect. Expected 'Total: 61', got '{content}'."