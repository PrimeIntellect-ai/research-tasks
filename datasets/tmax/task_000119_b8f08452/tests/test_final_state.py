# test_final_state.py

import os
import subprocess
import pytest

def test_pass_filter_script_exists():
    script_path = "/home/user/pass_filter.sh"
    assert os.path.isfile(script_path), f"Missing pass_filter.sh script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/pass_filter.sh"
    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    evil_bypassed = []
    clean_rejected = []

    for e_file in evil_files:
        result = subprocess.run(["bash", script_path, e_file], capture_output=True, text=True)
        # Expected: exit code 1, output REJECT
        if result.returncode != 1 or "REJECT" not in result.stdout:
            evil_bypassed.append(os.path.basename(e_file))

    for c_file in clean_files:
        result = subprocess.run(["bash", script_path, c_file], capture_output=True, text=True)
        # Expected: exit code 0, output ACCEPT
        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            clean_rejected.append(os.path.basename(c_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_msgs.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_rejected)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))