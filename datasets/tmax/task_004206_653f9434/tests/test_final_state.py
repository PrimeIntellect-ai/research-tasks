# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_validator_script_exists():
    script_path = "/home/user/validate_manifest.py"
    assert os.path.isfile(script_path), f"Validator script is missing at {script_path}"

def test_adversarial_corpus_validation():
    script_path = "/home/user/validate_manifest.py"
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.ttl"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.ttl"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    clean_failures = []
    for f in clean_files:
        res = subprocess.run(["python3", script_path, f], capture_output=True, text=True)
        output = res.stdout.strip()
        if output != "VALID":
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        res = subprocess.run(["python3", script_path, f], capture_output=True, text=True)
        output = res.stdout.strip()
        if output != "INVALID":
            evil_failures.append(os.path.basename(f))

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if errors:
        pytest.fail(" | ".join(errors))