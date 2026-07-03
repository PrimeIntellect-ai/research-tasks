# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/log_pipeline"

def test_mre_txt_content():
    mre_path = os.path.join(BASE_DIR, "mre.txt")
    assert os.path.isfile(mre_path), f"File {mre_path} is missing."

    with open(mre_path, "r") as f:
        content = f.read().strip()

    valid_lines = [
        "inputs/app2.log inputs/app6.log",
        "inputs/app6.log inputs/app2.log"
    ]
    assert content in valid_lines, f"mre.txt must contain exactly one of the deadlocking lines. Found: {content}"

def test_success_log_exists_and_content():
    success_path = os.path.join(BASE_DIR, "success.log")
    assert os.path.isfile(success_path), f"File {success_path} is missing. Did run_all.sh complete successfully?"

    with open(success_path, "r") as f:
        content = f.read().strip()

    assert content == "All jobs finished successfully", f"success.log has incorrect content: {content}"

def test_merge_logs_sh_modified():
    script_path = os.path.join(BASE_DIR, "merge_logs.sh")
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # The script should be modified to order the variables or lock files alphabetically
    # Look for bash string comparison operators or sort commands
    has_comparison = "<" in content or ">" in content or "sort" in content
    assert has_comparison, "merge_logs.sh does not seem to contain alphabetical comparison logic to prevent deadlocks."