# test_final_state.py

import os
import glob
import json
import subprocess
import pytest

def test_sanitizer_executable_exists():
    executable = "/home/user/sanitizer"
    assert os.path.exists(executable), f"Sanitizer executable not found at {executable}"
    assert os.path.isfile(executable), f"{executable} is not a file"
    assert os.access(executable, os.X_OK), f"{executable} is not executable"

def test_adversarial_corpus():
    executable = "/home/user/sanitizer"
    clean_dir = "/home/user/clean"
    evil_dir = "/home/user/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean files found in corpus"
    assert len(evil_files) > 0, "No evil files found in corpus"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for e_file in evil_files:
        with open(e_file, "rb") as f:
            result = subprocess.run([executable], stdin=f, capture_output=True, text=True)

        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            evil_bypassed.append(os.path.basename(e_file))

    # Test clean corpus
    expected_json = [
        {"node_id": "101", "label": "Person", "prop_value": "Developer"},
        {"node_id": "102", "label": "System", "prop_value": "Database"}
    ]

    for c_file in clean_files:
        with open(c_file, "rb") as f:
            result = subprocess.run([executable], stdin=f, capture_output=True, text=True)

        if result.returncode != 0:
            clean_modified.append(os.path.basename(c_file))
            continue

        try:
            parsed_json = json.loads(result.stdout)
            if parsed_json != expected_json:
                clean_modified.append(os.path.basename(c_file))
        except json.JSONDecodeError:
            clean_modified.append(os.path.basename(c_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/failed: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))