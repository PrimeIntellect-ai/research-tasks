# test_final_state.py
import os
import subprocess
import pytest

def test_classifier_exists_and_executable():
    script_path = "/home/user/classifier.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.path.isfile(script_path), f"Not a file: {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/classifier.sh"
    evil_dir = "/home/user/artifacts/evil/"
    clean_dir = "/home/user/artifacts/clean/"

    assert os.path.isdir(evil_dir), f"Missing evil directory: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing clean directory: {clean_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    bypassed_evil = []
    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        result = subprocess.run(["/bin/bash", script_path, filepath], capture_output=True)
        # Evil files MUST exit with a non-zero code
        if result.returncode == 0:
            bypassed_evil.append(f)

    modified_clean = []
    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        result = subprocess.run(["/bin/bash", script_path, filepath], capture_output=True)
        # Clean files MUST exit with 0
        if result.returncode != 0:
            modified_clean.append(f)

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))