# test_final_state.py

import os
import pytest

SECRET_FILE = "/home/user/secret.txt"
OUTPUT_LOG = "/home/user/output.log"

def test_secret_file_content():
    assert os.path.isfile(SECRET_FILE), f"{SECRET_FILE} is missing. You need to recover the secret and save it here."
    with open(SECRET_FILE, "r") as f:
        content = f.read().strip()
    assert content == "sk-9942b-secret-token", f"Content of {SECRET_FILE} is incorrect. Expected the recovered API token."

def test_output_log_content():
    assert os.path.isfile(OUTPUT_LOG), f"{OUTPUT_LOG} is missing. Did you run the fixed process_all.sh script?"
    with open(OUTPUT_LOG, "r") as f:
        content = f.read()

    expected_alpha = "PROCESSED: leaf_alpha WITH sk-9942b-secret-token"
    expected_beta = "PROCESSED: leaf_beta WITH sk-9942b-secret-token"

    assert expected_alpha in content, f"Expected to find '{expected_alpha}' in {OUTPUT_LOG}. Check your Rust parser logic and script."
    assert expected_beta in content, f"Expected to find '{expected_beta}' in {OUTPUT_LOG}. Check your Rust parser logic and script."