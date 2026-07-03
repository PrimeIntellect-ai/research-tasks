# test_final_state.py

import os
import subprocess
import pytest

def test_adversarial_corpus():
    script_path = "/home/user/filter.py"
    assert os.path.exists(script_path), f"Agent script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Agent script {script_path} is not a file."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".tar.gz")]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".tar.gz")]

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    clean_modified = []
    for f in clean_files:
        archive_path = os.path.join(clean_dir, f)
        ret = subprocess.run(["python3", script_path, archive_path], capture_output=True)
        if ret.returncode != 0:
            clean_modified.append(f)

    evil_bypassed = []
    for f in evil_files:
        archive_path = os.path.join(evil_dir, f)
        ret = subprocess.run(["python3", script_path, archive_path], capture_output=True)
        if ret.returncode != 1:
            evil_bypassed.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)