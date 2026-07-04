# test_final_state.py

import os
import glob
import subprocess
import pytest

def run_detector(csv_path):
    cmd = ["python3", "/home/user/detector.py", "--input", csv_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_detector_script_exists():
    script_path = "/home/user/detector.py"
    assert os.path.exists(script_path), f"Detector script missing at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

def test_adversarial_corpus_classification():
    evil_dir = "/app/holdout/evil/"
    clean_dir = "/app/holdout/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(evil_files) > 0, f"No evil files found in holdout corpus at {evil_dir}"
    assert len(clean_files) > 0, f"No clean files found in holdout corpus at {clean_dir}"

    evil_bypassed = []
    for f in evil_files:
        output = run_detector(f)
        if output != "EVIL":
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        output = run_detector(f)
        if output != "CLEAN":
            clean_modified.append(os.path.basename(f))

    total_evil = len(evil_files)
    total_clean = len(clean_files)

    err_msgs = []
    if evil_bypassed:
        err_msgs.append(f"{len(evil_bypassed)} of {total_evil} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        err_msgs.append(f"{len(clean_modified)} of {total_clean} clean modified: {', '.join(clean_modified)}")

    if err_msgs:
        pytest.fail(" | ".join(err_msgs))