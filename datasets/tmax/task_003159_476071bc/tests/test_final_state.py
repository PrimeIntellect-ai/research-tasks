# test_final_state.py

import os
import subprocess
import pytest

def test_batch_id_recovered():
    """
    Checks that the correct Batch ID was extracted from the screenshot
    and written to the specified log file.
    """
    log_path = "/home/user/batch_id_recovery.log"
    assert os.path.exists(log_path), f"Log file {log_path} not found. Did you extract the Batch ID?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "BATCH-77A90X" in content, f"Extracted Batch ID is incorrect or missing in {log_path}."

def test_validate_script_adversarial_corpus():
    """
    Tests the standalone validate.py script against the evil and clean corpora.
    Pass criterion: 100% of evil rejected (exit code 1 and stdout 'UNSAFE') AND 
    100% of clean preserved (exit code 0 and stdout 'SAFE')
    """
    script_path = "/home/user/validate.py"
    assert os.path.exists(script_path), f"Validation script {script_path} not found."

    evil_corpus_path = "/app/corpora/evil_filenames.txt"
    clean_corpus_path = "/app/corpora/clean_filenames.txt"

    assert os.path.exists(evil_corpus_path), f"Evil corpus missing at {evil_corpus_path}"
    assert os.path.exists(clean_corpus_path), f"Clean corpus missing at {clean_corpus_path}"

    with open(evil_corpus_path, "r") as f:
        evil_files = [line.strip("\n") for line in f if line.strip("\n")]

    with open(clean_corpus_path, "r") as f:
        clean_files = [line.strip("\n") for line in f if line.strip("\n")]

    evil_bypassed = []
    for evil_file in evil_files:
        res = subprocess.run(["python3", script_path, evil_file], capture_output=True, text=True)
        if res.returncode != 1 or res.stdout.strip() != "UNSAFE":
            evil_bypassed.append(evil_file)

    clean_modified = []
    for clean_file in clean_files:
        res = subprocess.run(["python3", script_path, clean_file], capture_output=True, text=True)
        if res.returncode != 0 or res.stdout.strip() != "SAFE":
            clean_modified.append(clean_file)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {evil_bypassed}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {clean_modified}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))