# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_validator_script_exists():
    assert os.path.isfile("/home/user/validator.py"), "/home/user/validator.py does not exist."

def test_adversarial_corpus():
    validator_path = "/home/user/validator.py"

    clean_files = glob.glob("/app/clean/*.json")
    evil_files = glob.glob("/app/evil/*.json")

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_rejected = []
    for clean_file in clean_files:
        result = subprocess.run(
            ["python3", validator_path, clean_file],
            capture_output=True,
            text=True
        )
        # Clean files MUST exit 0
        if result.returncode != 0 or "VALID" not in result.stdout:
            clean_rejected.append(os.path.basename(clean_file))

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", validator_path, evil_file],
            capture_output=True,
            text=True
        )
        # Evil files MUST exit 1
        if result.returncode != 1 or "INVALID" not in result.stdout:
            evil_bypassed.append(os.path.basename(evil_file))

    error_messages = []
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean files rejected: {', '.join(clean_rejected)}")
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil files bypassed: {', '.join(evil_bypassed)}")

    assert not error_messages, " | ".join(error_messages)