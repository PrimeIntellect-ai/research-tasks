# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_adversarial_corpus():
    script_path = "/home/user/analyze.sh"
    clean_base = "/opt/corpus/clean"
    evil_base = "/opt/corpus/evil"

    clean_dirs = [os.path.join(clean_base, d) for d in os.listdir(clean_base) if os.path.isdir(os.path.join(clean_base, d))]
    evil_dirs = [os.path.join(evil_base, d) for d in os.listdir(evil_base) if os.path.isdir(os.path.join(evil_base, d))]

    assert len(clean_dirs) > 0, f"No subdirectories found in {clean_base}"
    assert len(evil_dirs) > 0, f"No subdirectories found in {evil_base}"

    clean_failures = []
    evil_failures = []

    for d in clean_dirs:
        result = subprocess.run([script_path, d], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(d))

    for d in evil_dirs:
        result = subprocess.run([script_path, d], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(d))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_dirs)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_dirs)} evil bypassed: {', '.join(evil_failures)}")

    assert not error_messages, " | ".join(error_messages)