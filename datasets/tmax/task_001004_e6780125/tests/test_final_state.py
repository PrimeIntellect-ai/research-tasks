# test_final_state.py

import os
import subprocess
import pytest

def test_detector_script_exists():
    assert os.path.isfile('/home/user/detector.sh'), "The detector script /home/user/detector.sh is missing."

def test_adversarial_corpus_classification():
    evil_dir = '/app/corpora/evil'
    clean_dir = '/app/corpora/clean'
    detector_script = '/home/user/detector.sh'

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    for fpath in evil_files:
        result = subprocess.run(['bash', detector_script, fpath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(fpath))

    clean_modified = []
    for fpath in clean_files:
        result = subprocess.run(['bash', detector_script, fpath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(fpath))

    total_evil = len(evil_files)
    total_clean = len(clean_files)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {total_evil} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {total_clean} clean modified/rejected: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))