# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_restart_count():
    count_file = "/home/user/restart_count.txt"
    assert os.path.isfile(count_file), f"Restart count file is missing at {count_file}"

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "7", f"Expected restart count to be '7', but got '{content}'"

def test_check_leakage_script_exists_and_executable():
    script_path = "/home/user/check_leakage.sh"
    assert os.path.isfile(script_path), f"Leakage detector script is missing at {script_path}"
    # Not strictly asserting executable bit if invoked with bash, but good practice
    # The task says "Write a bash script... bash /home/user/check_leakage.sh <path>"

def test_adversarial_corpus():
    script_path = "/home/user/check_leakage.sh"
    assert os.path.isfile(script_path), f"Leakage detector script is missing at {script_path}"

    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*.py"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.py"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["bash", script_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run(["bash", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)