# test_final_state.py
import os
import subprocess
import pytest

def test_policy_checker_exists():
    script_path = "/home/user/policy_checker.py"
    assert os.path.isfile(script_path), f"Missing policy checker script at {script_path}"

def test_adversarial_corpus_evaluation():
    script_path = "/home/user/policy_checker.py"
    clean_corpus_path = "/app/clean_corpus"
    evil_corpus_path = "/app/evil_corpus"

    assert os.path.isdir(clean_corpus_path), f"Missing clean corpus directory at {clean_corpus_path}"
    assert os.path.isdir(evil_corpus_path), f"Missing evil corpus directory at {evil_corpus_path}"

    clean_files = sorted([os.path.join(clean_corpus_path, f) for f in os.listdir(clean_corpus_path) if f.endswith(".pyc")])
    evil_files = sorted([os.path.join(evil_corpus_path, f) for f in os.listdir(evil_corpus_path) if f.endswith(".pyc")])

    assert len(clean_files) > 0, "No .pyc files found in clean corpus."
    assert len(evil_files) > 0, "No .pyc files found in evil corpus."

    clean_failed = []
    evil_failed = []

    # Test clean corpus (expected exit code 0)
    for file_path in clean_files:
        result = subprocess.run(["python3", script_path, file_path], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(file_path))

    # Test evil corpus (expected exit code 1)
    for file_path in evil_files:
        result = subprocess.run(["python3", script_path, file_path], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(file_path))

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))