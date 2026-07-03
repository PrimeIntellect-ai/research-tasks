# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitize.sh"
EVIL_CORPUS_DIR = "/app/verifier_corpus/evil"
CLEAN_CORPUS_DIR = "/app/verifier_corpus/clean"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist. You must create the filter script at this path."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable. Did you forget to run 'chmod +x'?"

def test_adversarial_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.jsonl"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.jsonl"))

    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}."
    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus: all lines must be dropped (stdout should be empty)
    for e_file in evil_files:
        with open(e_file, 'r') as f:
            content = f.read()

        try:
            proc = subprocess.run([SCRIPT_PATH], input=content, text=True, capture_output=True, timeout=5)
            if proc.stdout.strip():
                evil_bypassed.append(os.path.basename(e_file))
        except subprocess.TimeoutExpired:
            evil_bypassed.append(os.path.basename(e_file) + " (timeout)")
        except Exception as e:
            evil_bypassed.append(os.path.basename(e_file) + f" (error: {e})")

    # Test clean corpus: all lines must be preserved (stdout perfectly matches stdin)
    for c_file in clean_files:
        with open(c_file, 'r') as f:
            content = f.read()

        try:
            proc = subprocess.run([SCRIPT_PATH], input=content, text=True, capture_output=True, timeout=5)
            # Compare stripped versions to ignore trailing newlines at the EOF
            if proc.stdout.strip() != content.strip():
                clean_modified.append(os.path.basename(c_file))
        except subprocess.TimeoutExpired:
            clean_modified.append(os.path.basename(c_file) + " (timeout)")
        except Exception as e:
            clean_modified.append(os.path.basename(c_file) + f" (error: {e})")

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))