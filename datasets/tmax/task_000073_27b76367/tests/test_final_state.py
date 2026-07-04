# test_final_state.py

import os
import subprocess
import pytest

def test_jwt_filter_exists():
    script_path = "/home/user/jwt_filter.py"
    assert os.path.isfile(script_path), f"Expected script at {script_path} is missing."

def test_adversarial_corpus():
    script_path = "/home/user/jwt_filter.py"
    evil_corpus = "/app/verifier/corpus/evil"
    clean_corpus = "/app/verifier/corpus/clean"

    assert os.path.isdir(evil_corpus), f"Evil corpus directory {evil_corpus} is missing."
    assert os.path.isdir(clean_corpus), f"Clean corpus directory {clean_corpus} is missing."

    evil_files = [os.path.join(evil_corpus, f) for f in os.listdir(evil_corpus) if os.path.isfile(os.path.join(evil_corpus, f))]
    clean_files = [os.path.join(clean_corpus, f) for f in os.listdir(clean_corpus) if os.path.isfile(os.path.join(clean_corpus, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        result = subprocess.run(["python3", script_path, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus
    for clean_file in clean_files:
        result = subprocess.run(["python3", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)