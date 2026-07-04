# test_final_state.py

import os
import subprocess
import pytest

def test_detector_script_exists():
    script_path = "/home/user/detector.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_adversarial_corpus():
    script_path = "/home/user/detector.sh"
    evil_dir = "/hidden/corpus/evil"
    clean_dir = "/hidden/corpus/clean"

    assert os.path.isdir(evil_dir), f"Missing directory: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing directory: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in the evil corpus."
    assert len(clean_files) > 0, "No files found in the clean corpus."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["bash", script_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_flagged = []
    for clean_file in clean_files:
        result = subprocess.run(["bash", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_flagged.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_flagged:
        errors.append(f"{len(clean_flagged)} of {len(clean_files)} clean modified/flagged: {', '.join(clean_flagged)}")

    assert not errors, " | ".join(errors)