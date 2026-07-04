# test_final_state.py
import os
import shutil
import subprocess
import pytest

EVIL_DIR = "/app/corpora/evil"
CLEAN_DIR = "/app/corpora/clean"
SCRIPT_PATH = "/home/user/filter.sh"
TEST_DIR = "/tmp/test_eval"

def test_filter_script_behavior():
    # 1. Verify script exists and is executable
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

    # 2. Set up the testing directory
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    evil_files = os.listdir(EVIL_DIR)
    clean_files = os.listdir(CLEAN_DIR)

    for f in evil_files:
        shutil.copy2(os.path.join(EVIL_DIR, f), TEST_DIR)
    for f in clean_files:
        shutil.copy2(os.path.join(CLEAN_DIR, f), TEST_DIR)

    # 3. Execute the student's script
    result = subprocess.run([SCRIPT_PATH, TEST_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # 4. Verify the .quarantine directory exists
    quarantine_dir = os.path.join(TEST_DIR, ".quarantine")
    assert os.path.isdir(quarantine_dir), f"The .quarantine directory was not created in {TEST_DIR}."

    # 5. Check adversarial corpus criteria
    evil_bypassed = []
    for f in evil_files:
        if not os.path.exists(os.path.join(quarantine_dir, f)):
            evil_bypassed.append(f)

    clean_modified = []
    for f in clean_files:
        if not os.path.exists(os.path.join(TEST_DIR, f)) or os.path.exists(os.path.join(quarantine_dir, f)):
            clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))