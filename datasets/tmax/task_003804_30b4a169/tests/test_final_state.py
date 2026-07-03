# test_final_state.py
import os
import re

def test_redacted_log_content():
    redacted_log_path = "/home/user/app_redacted.log"
    assert os.path.exists(redacted_log_path), f"File {redacted_log_path} does not exist."
    assert os.path.isfile(redacted_log_path), f"Path {redacted_log_path} is not a file."

    with open(redacted_log_path, "r") as f:
        content = f.read()

    assert "AKIA" not in content, "Found 'AKIA' in the redacted log; AWS keys were not fully redacted."
    assert "[REDACTED]" in content, "Did not find '[REDACTED]' in the redacted log."

    expected_content = """System initialized.
User login: [REDACTED] success.
Connecting to backend.
Error: [REDACTED] invalid permissions.
Processing batch 1."""

    assert content.strip() == expected_content.strip(), f"The content of {redacted_log_path} does not match the expected redacted output."

def test_recovered_password():
    pass_path = "/home/user/recovered_pass.txt"
    assert os.path.exists(pass_path), f"File {pass_path} does not exist."
    assert os.path.isfile(pass_path), f"Path {pass_path} is not a file."

    with open(pass_path, "r") as f:
        content = f.read()

    assert content == "OldSecr3tP4ss!", f"The recovered password in {pass_path} is incorrect. Expected 'OldSecr3tP4ss!' but got '{content}'."

def test_run_secure_script():
    script_path = "/home/user/run_secure.sh"
    assert os.path.exists(script_path), f"File {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

    with open(script_path, "r") as f:
        content = f.read()

    # Check for ulimit
    assert re.search(r"ulimit\s+-n\s+50", content) or re.search(r"ulimit\s+.*50", content), \
        f"The script {script_path} does not appear to restrict open file descriptors to 50 using ulimit."

    # Check for env -i
    assert "env -i" in content, \
        f"The script {script_path} does not appear to use 'env -i' to create an empty environment."

    # Check for SECRET_KEY assignment
    assert "SECRET_KEY=" in content, \
        f"The script {script_path} does not appear to set the SECRET_KEY environment variable."