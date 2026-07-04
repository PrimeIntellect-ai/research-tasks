# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/artifact_filter/target/release/artifact_filter"
EVIL_DIR = "/app/corpora/evil/"
CLEAN_DIR = "/app/corpora/clean/"

def test_binary_exists():
    assert os.path.exists(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.path.isfile(BINARY_PATH), f"Path {BINARY_PATH} is not a file"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_adversarial_corpus_filtering():
    assert os.path.exists(EVIL_DIR) and os.path.isdir(EVIL_DIR), f"Evil corpus directory missing at {EVIL_DIR}"
    assert os.path.exists(CLEAN_DIR) and os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing at {CLEAN_DIR}"

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    assert len(evil_files) > 0, f"No files found in {EVIL_DIR}"
    assert len(clean_files) > 0, f"No files found in {CLEAN_DIR}"

    evil_bypassed = []
    for evil_file in evil_files:
        res = subprocess.run([BINARY_PATH, evil_file], capture_output=True, text=True)
        if res.returncode != 1 or res.stdout.strip() != "EVIL":
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        res = subprocess.run([BINARY_PATH, clean_file], capture_output=True, text=True)
        if res.returncode != 0 or res.stdout.strip() != "CLEAN":
            clean_modified.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}{'...' if len(evil_bypassed) > 5 else ''}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified[:5])}{'...' if len(clean_modified) > 5 else ''}")

    if errors:
        pytest.fail(" | ".join(errors))