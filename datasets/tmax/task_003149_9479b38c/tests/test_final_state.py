# test_final_state.py

import os
import subprocess
import pytest

def test_spike_frames_extracted():
    """Verify that the correct frame numbers were extracted and saved."""
    file_path = "/home/user/spike_frames.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Task 1 was not completed."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_frames = "145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160"
    assert content == expected_frames, f"Extracted frames do not match the expected output. Got: '{content}'"

def test_cost_filter_adversarial_corpus():
    """Verify that the cost_filter.py script correctly rejects evil directories and accepts clean ones."""
    script_path = "/home/user/cost_filter.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing. Task 2 was not completed."

    evil_corpus_path = "/app/corpora/evil/"
    clean_corpus_path = "/app/corpora/clean/"

    assert os.path.isdir(evil_corpus_path), f"Evil corpus path {evil_corpus_path} is missing."
    assert os.path.isdir(clean_corpus_path), f"Clean corpus path {clean_corpus_path} is missing."

    evil_dirs = [os.path.join(evil_corpus_path, d) for d in os.listdir(evil_corpus_path) if os.path.isdir(os.path.join(evil_corpus_path, d))]
    clean_dirs = [os.path.join(clean_corpus_path, d) for d in os.listdir(clean_corpus_path) if os.path.isdir(os.path.join(clean_corpus_path, d))]

    evil_bypassed = []
    for d in evil_dirs:
        result = subprocess.run(["python3", script_path, d], capture_output=True, text=True)
        # Must print REJECT and exit with 1
        if result.returncode != 1 or "REJECT" not in result.stdout:
            evil_bypassed.append(os.path.basename(d))

    clean_modified = []
    for d in clean_dirs:
        result = subprocess.run(["python3", script_path, d], capture_output=True, text=True)
        # Must print ACCEPT and exit with 0
        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            clean_modified.append(os.path.basename(d))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_dirs)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_dirs)} clean modified: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, " ; ".join(error_messages)