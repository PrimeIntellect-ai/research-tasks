# test_final_state.py

import os
import subprocess
import pytest

def test_detect_papermill():
    script_path = "/home/user/detect_papermill.sh"

    # Check if the script exists and is executable
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    evil_corpus_dir = "/verify/corpus/evil"
    clean_corpus_dir = "/verify/corpus/clean"

    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]
    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        result = subprocess.run([script_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus
    for clean_file in clean_files:
        result = subprocess.run([script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_messages)