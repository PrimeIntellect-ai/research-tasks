# test_final_state.py

import os
import subprocess
import pytest

def get_detect_script():
    user_dir = "/home/user"
    if not os.path.isdir(user_dir):
        return None
    for file in os.listdir(user_dir):
        if file.startswith("detect_leak"):
            full_path = os.path.join(user_dir, file)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
    # Fallback to checking if it's a python script without execute bit
    for file in os.listdir(user_dir):
        if file.startswith("detect_leak") and file.endswith(".py"):
            return os.path.join(user_dir, file)
    return None

def test_detect_leak_executable_exists():
    script_path = get_detect_script()
    assert script_path is not None, "Could not find an executable script starting with 'detect_leak' in /home/user/"

def test_adversarial_corpus():
    script_path = get_detect_script()
    assert script_path is not None, "Script not found."

    evil_dir = "/app/eval/evil"
    clean_dir = "/app/eval/clean"

    assert os.path.isdir(evil_dir), f"Missing evil eval directory at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing clean eval directory at {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    # Helper to run script
    def run_script(filepath):
        if script_path.endswith(".py") and not os.access(script_path, os.X_OK):
            cmd = ["python3", script_path, filepath]
        else:
            cmd = [script_path, filepath]
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode

    # Test evil corpus
    for filepath in evil_files:
        code = run_script(filepath)
        if code != 1:
            evil_bypassed.append(os.path.basename(filepath))

    # Test clean corpus
    for filepath in clean_files:
        code = run_script(filepath)
        if code != 0:
            clean_modified.append(os.path.basename(filepath))

    total_evil = len(evil_files)
    total_clean = len(clean_files)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {total_evil} evil bypassed (expected exit code 1): {', '.join(evil_bypassed[:5])}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {total_clean} clean modified/rejected (expected exit code 0): {', '.join(clean_modified[:5])}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))