# test_final_state.py

import os
import subprocess
import pytest

def test_detector_script_exists_and_executable():
    script_path = "/home/user/detector.py"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    # The instructions say "Ensure /home/user/detector.py is executable"
    # We can run it via `python3 /home/user/detector.py` or `./detector.py`
    # We will test execution via `python3` to be safe, but checking x-bit is good.
    assert os.access(script_path, os.X_OK) or os.access(script_path, os.R_OK), f"Script at {script_path} must be readable/executable"

def test_adversarial_corpus():
    script_path = "/home/user/detector.py"
    clean_corpus = "/app/test_corpus/clean"
    evil_corpus = "/app/test_corpus/evil"

    assert os.path.exists(clean_corpus), f"Missing clean corpus dir: {clean_corpus}"
    assert os.path.exists(evil_corpus), f"Missing evil corpus dir: {evil_corpus}"

    clean_batches = sorted([os.path.join(clean_corpus, d) for d in os.listdir(clean_corpus) if os.path.isdir(os.path.join(clean_corpus, d))])
    evil_batches = sorted([os.path.join(evil_corpus, d) for d in os.listdir(evil_corpus) if os.path.isdir(os.path.join(evil_corpus, d))])

    assert len(clean_batches) > 0, "No clean batches found in test corpus."
    assert len(evil_batches) > 0, "No evil batches found in test corpus."

    clean_failed = []
    for batch in clean_batches:
        result = subprocess.run(["python3", script_path, batch], capture_output=True)
        # Clean batches must exit with 0
        if result.returncode != 0:
            clean_failed.append(os.path.basename(batch))

    evil_bypassed = []
    for batch in evil_batches:
        result = subprocess.run(["python3", script_path, batch], capture_output=True)
        # Evil batches must exit with 1
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(batch))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_batches)} clean modified (rejected instead of accepted): {', '.join(clean_failed)}")
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_batches)} evil bypassed (accepted instead of rejected): {', '.join(evil_bypassed)}")

    assert not error_messages, " | ".join(error_messages)