# test_final_state.py

import os
import glob
import subprocess

def test_query_validator_exists():
    """Ensure the user created the query validator script."""
    script_path = "/home/user/query_validator.py"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.path.isfile(script_path), f"Not a file: {script_path}"

def test_adversarial_corpus():
    """Test the script against the clean and evil corpora."""
    script_path = "/home/user/query_validator.py"

    clean_dir = "/app/clean/"
    evil_dir = "/app/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*.cypher"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.cypher"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(["python3", script_path, cf], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "VALID":
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(["python3", script_path, ef], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "INVALID":
            evil_failures.append(os.path.basename(ef))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean files rejected/failed: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil files bypassed: {', '.join(evil_failures)}")

    if error_messages:
        assert False, " | ".join(error_messages)