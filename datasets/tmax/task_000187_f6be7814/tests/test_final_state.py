# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_recovered_log():
    """Verify the recovered log file exists and contains the correct crash entry."""
    log_path = "/home/user/recovered_system.log"
    assert os.path.isfile(log_path), f"Missing recovered log file: {log_path}"
    with open(log_path, "r", errors="replace") as f:
        content = f.read()
    assert "2024-05-12 09:15:33" in content, "Recovered log does not contain the entry for the crash timestamp (2024-05-12 09:15:33)."

def test_crash_cause():
    """Verify the crash cause file contains the exact malicious payload."""
    cause_path = "/home/user/crash_cause.txt"
    assert os.path.isfile(cause_path), f"Missing crash cause file: {cause_path}"
    with open(cause_path, "r", errors="replace") as f:
        content = f.read().strip()
    expected = '/var/drop/payload; rm -rf /; echo "hacked"'
    assert content == expected, f"Crash cause file content mismatch. Expected: '{expected}', Got: '{content}'"

def test_sanitizer_exists_and_executable():
    """Verify the sanitizer binary is compiled and executable."""
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Missing compiled sanitizer executable: {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer is not executable: {sanitizer_path}"

def test_sanitizer_adversarial_corpus():
    """Evaluate the sanitizer against the strict adversarial corpus."""
    sanitizer_path = "/home/user/sanitizer"
    evil_corpus = glob.glob("/app/corpus/evil/*")
    clean_corpus = glob.glob("/app/corpus/clean/*")

    assert len(evil_corpus) > 0, "Evil corpus is empty or missing in the environment."
    assert len(clean_corpus) > 0, "Clean corpus is empty or missing in the environment."

    evil_bypassed = []
    for evil_file in evil_corpus:
        with open(evil_file, "rb") as f:
            payload = f.read()
        proc = subprocess.run([sanitizer_path], input=payload, capture_output=True)
        # The sanitizer MUST reject (exit code != 0) evil inputs
        if proc.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_corpus:
        with open(clean_file, "rb") as f:
            payload = f.read()
        proc = subprocess.run([sanitizer_path], input=payload, capture_output=True)
        # The sanitizer MUST accept (exit code == 0) clean inputs
        if proc.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_corpus)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_corpus)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail("Sanitizer failed adversarial checks. " + "; ".join(error_msgs))