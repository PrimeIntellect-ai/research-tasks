# test_final_state.py

import os
import subprocess
import pytest

def test_crash_time():
    crash_file = "/home/user/crash_time.txt"
    assert os.path.isfile(crash_file), f"File {crash_file} is missing."
    with open(crash_file, "r") as f:
        content = f.read().strip()
    assert content == "17", f"Expected crash time to be 17, but got {content}."

def test_sanitize_script_exists_and_executable():
    script_path = "/home/user/sanitize.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_adversarial_corpus():
    script_path = "/home/user/sanitize.sh"
    clean_dir = "/app/verifier/clean"
    evil_dir = "/app/verifier/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(["bash", script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(["bash", script_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    errors = []
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    assert not clean_failures and not evil_failures, "Adversarial corpus verification failed:\n" + "\n".join(errors)