# test_final_state.py

import os
import pytest

APP_DIR = "/home/user/app"
HASH_C = os.path.join(APP_DIR, "hash.c")
APP_BIN = os.path.join(APP_DIR, "app")
SUCCESS_LOG = os.path.join(APP_DIR, "success.log")

def test_hash_c_patched():
    """Verify that hash.c has been patched to rename the function."""
    assert os.path.isfile(HASH_C), f"File {HASH_C} is missing."
    with open(HASH_C, "r") as f:
        content = f.read()
    assert "calculate_hash" in content, f"{HASH_C} does not contain 'calculate_hash'. The patch was likely not applied."
    assert "calc_hsh" not in content, f"{HASH_C} still contains 'calc_hsh'. The patch was likely not applied correctly."

def test_app_binary_exists():
    """Verify that the application was successfully built."""
    assert os.path.isfile(APP_BIN), f"Binary {APP_BIN} does not exist. Did the build succeed?"
    assert os.access(APP_BIN, os.X_OK), f"Binary {APP_BIN} is not executable."

def test_success_log():
    """Verify that the success.log contains the expected output."""
    assert os.path.isfile(SUCCESS_LOG), f"Log file {SUCCESS_LOG} does not exist. Did you run the app and redirect output?"
    with open(SUCCESS_LOG, "r") as f:
        content = f.read().strip()

    expected = "Hash: 420"
    assert content == expected, f"Content of {SUCCESS_LOG} is incorrect. Expected '{expected}', got '{content}'."