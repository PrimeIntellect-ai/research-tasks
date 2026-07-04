# test_final_state.py

import os
import pytest

def test_key_file():
    key_path = "/home/user/key.txt"
    assert os.path.isfile(key_path), f"File {key_path} does not exist. Phase 1 incomplete."

    with open(key_path, 'r') as f:
        content = f.read().strip()

    expected_key = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
    assert content == expected_key, f"Content of {key_path} is incorrect. Expected {expected_key}, got {content}."

def test_token_file():
    token_path = "/home/user/.hidden_token_file"
    assert os.path.isfile(token_path), f"File {token_path} does not exist. Phase 2 incomplete."

    with open(token_path, 'r') as f:
        content = f.read().strip()

    expected_token = "TOKEN_OK"
    assert content == expected_token, f"Content of {token_path} is incorrect. Expected {expected_token}, got {content}."

def test_total_file():
    total_path = "/home/user/total.txt"
    assert os.path.isfile(total_path), f"File {total_path} does not exist. Did you run the script?"

    with open(total_path, 'r') as f:
        content = f.read().strip()

    expected_total = "Total: 110.95"
    assert content == expected_total, f"Content of {total_path} is incorrect. Expected '{expected_total}', got '{content}'. Ensure you fixed the precision bug and ran the script."

def test_process_py_uses_decimal():
    process_path = "/home/user/analytics_repo/process.py"
    assert os.path.isfile(process_path), f"File {process_path} does not exist."

    with open(process_path, 'r') as f:
        content = f.read()

    assert "decimal" in content or "Decimal" in content, "The process.py script does not appear to use the 'decimal' module as requested."