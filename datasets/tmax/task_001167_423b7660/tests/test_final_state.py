# test_final_state.py

import os
import subprocess
import pytest

LINTER_PATH = "/home/user/config_linter.py"
EVIL_CORPUS = "/var/opt/verifier/corpus/evil/"
CLEAN_CORPUS = "/var/opt/verifier/corpus/clean/"

def test_linter_exists_and_executable():
    assert os.path.exists(LINTER_PATH), f"Linter script {LINTER_PATH} is missing."
    assert os.path.isfile(LINTER_PATH), f"{LINTER_PATH} is not a file."
    assert os.access(LINTER_PATH, os.X_OK), f"{LINTER_PATH} is not executable."

def test_linter_behavior_against_corpora():
    assert os.path.exists(EVIL_CORPUS), f"Evil corpus missing at {EVIL_CORPUS}"
    assert os.path.exists(CLEAN_CORPUS), f"Clean corpus missing at {CLEAN_CORPUS}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    for f in evil_files:
        file_path = os.path.join(EVIL_CORPUS, f)
        try:
            result = subprocess.run([LINTER_PATH, file_path], capture_output=True, timeout=5)
            if result.returncode == 0:
                evil_bypassed.append(f)
        except Exception as e:
            pytest.fail(f"Execution failed for {file_path}: {e}")

    clean_rejected = []
    for f in clean_files:
        file_path = os.path.join(CLEAN_CORPUS, f)
        try:
            result = subprocess.run([LINTER_PATH, file_path], capture_output=True, timeout=5)
            if result.returncode != 0:
                clean_rejected.append(f)
        except Exception as e:
            pytest.fail(f"Execution failed for {file_path}: {e}")

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_msgs.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))