# test_final_state.py
import os
import json
import subprocess
import pytest

def test_validator_script_exists():
    assert os.path.isfile("/home/user/validator.py"), "Validator script is missing at /home/user/validator.py"

def test_validator_classifies_corpora():
    validator_path = "/home/user/validator.py"
    evil_input = "/app/test_corpora/evil"
    clean_input = "/app/test_corpora/clean"
    evil_output = "/tmp/evil_res.json"
    clean_output = "/tmp/clean_res.json"

    # Ensure output files are removed before running
    if os.path.exists(evil_output):
        os.remove(evil_output)
    if os.path.exists(clean_output):
        os.remove(clean_output)

    # Run on evil corpus
    evil_run = subprocess.run(["python3", validator_path, "--input", evil_input, "--output", evil_output], capture_output=True, text=True)
    assert evil_run.returncode == 0, f"Validator failed on evil corpus. Stderr: {evil_run.stderr}"
    assert os.path.isfile(evil_output), f"Validator did not produce output at {evil_output}"

    # Run on clean corpus
    clean_run = subprocess.run(["python3", validator_path, "--input", clean_input, "--output", clean_output], capture_output=True, text=True)
    assert clean_run.returncode == 0, f"Validator failed on clean corpus. Stderr: {clean_run.stderr}"
    assert os.path.isfile(clean_output), f"Validator did not produce output at {clean_output}"

    with open(evil_output, "r") as f:
        evil_res = json.load(f)

    with open(clean_output, "r") as f:
        clean_res = json.load(f)

    # Check evil corpus
    expected_evil_files = [f for f in os.listdir(evil_input) if f.endswith(".tar") or f.endswith(".tar.gz")]
    evil_bypassed = []
    for f in expected_evil_files:
        if evil_res.get(f) != "EVIL":
            evil_bypassed.append(f)

    # Check clean corpus
    expected_clean_files = [f for f in os.listdir(clean_input) if f.endswith(".tar") or f.endswith(".tar.gz")]
    clean_modified = []
    for f in expected_clean_files:
        if clean_res.get(f) != "CLEAN":
            clean_modified.append(f)

    error_msg = ""
    if evil_bypassed:
        error_msg += f"{len(evil_bypassed)} of {len(expected_evil_files)} evil bypassed: {', '.join(evil_bypassed)}. "
    if clean_modified:
        error_msg += f"{len(clean_modified)} of {len(expected_clean_files)} clean modified/rejected: {', '.join(clean_modified)}."

    assert not evil_bypassed and not clean_modified, error_msg.strip()