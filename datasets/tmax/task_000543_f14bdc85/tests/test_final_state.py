# test_final_state.py

import os
import pytest

def test_enforce_sh_exists_and_executable():
    enforce_sh = "/home/user/enforce.sh"
    assert os.path.isfile(enforce_sh), f"{enforce_sh} does not exist."
    assert os.access(enforce_sh, os.X_OK), f"{enforce_sh} is not executable."

def test_encrypted_log_content():
    encrypted_log = "/home/user/encrypted.log"
    assert os.path.isfile(encrypted_log), f"{encrypted_log} does not exist."

    with open(encrypted_log, "r") as f:
        content = f.read().strip()

    expected_hex = "104c4d4d46475a404b50424b5540415d404b5f4741405a3026362325372132365a435a4e404b464a475a4043422e0a25424a4f46475a4b4d454b415d404b5f4741405a3026362325372132365a444d505a415a465a43464f4b4c2e0a"

    assert content == expected_hex, f"Content of {encrypted_log} is incorrect. Expected {expected_hex}, got {content}"

def test_diff_analysis_content():
    diff_analysis = "/home/user/diff_analysis.txt"
    assert os.path.isfile(diff_analysis), f"{diff_analysis} does not exist."

    with open(diff_analysis, "r") as f:
        content = f.read().strip()

    expected_diff = "00000000000003"
    assert content == expected_diff, f"Content of {diff_analysis} is incorrect. Expected {expected_diff}, got {content}"