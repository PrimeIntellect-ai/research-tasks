# test_final_state.py
import os
import subprocess
import pytest

def test_filter_script_exists_and_executable():
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_adversarial_corpus():
    script_path = "/home/user/filter.sh"
    evil_base = "/app/corpora/evil"
    clean_base = "/app/corpora/clean"

    evil_bypassed = []
    clean_rejected = []

    # Check evil corpus
    if os.path.isdir(evil_base):
        for item in sorted(os.listdir(evil_base)):
            item_path = os.path.join(evil_base, item)
            if not os.path.isdir(item_path):
                continue

            result = subprocess.run([script_path, item_path], capture_output=True)
            if result.returncode == 0:
                evil_bypassed.append(item)

    # Check clean corpus
    if os.path.isdir(clean_base):
        for item in sorted(os.listdir(clean_base)):
            item_path = os.path.join(clean_base, item)
            if not os.path.isdir(item_path):
                continue

            result = subprocess.run([script_path, item_path], capture_output=True)
            if result.returncode != 0:
                clean_rejected.append(item)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} evil items bypassed (should have been rejected): {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} clean items rejected (should have been accepted): {', '.join(clean_rejected)}")

    assert not evil_bypassed and not clean_rejected, " | ".join(error_messages)