# test_final_state.py

import os
import subprocess
import pytest

def test_filter_script_exists():
    assert os.path.isfile("/home/user/filter.py"), "/home/user/filter.py does not exist."

def test_adversarial_corpus():
    script_path = "/home/user/filter.py"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), "Clean corpus dir missing"
    assert os.path.isdir(evil_dir), "Evil corpus dir missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.npy')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.npy')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    bypassed_evil = []
    modified_clean = []

    # Test clean corpus (should accept -> exit code 0)
    for f in clean_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(f))

    # Test evil corpus (should reject -> exit code 1)
    for f in evil_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode == 0:
            bypassed_evil.append(os.path.basename(f))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))