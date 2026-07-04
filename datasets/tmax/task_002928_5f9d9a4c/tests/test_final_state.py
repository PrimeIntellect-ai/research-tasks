# test_final_state.py
import os
import glob
import subprocess
import pytest

THRESHOLD_FILE = "/home/user/threshold.txt"
SCRIPT_FILE = "/home/user/detect.py"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_threshold_file():
    assert os.path.isfile(THRESHOLD_FILE), f"Threshold file missing at {THRESHOLD_FILE}"
    with open(THRESHOLD_FILE, "r") as f:
        content = f.read().strip()
    assert content == "14", f"Expected threshold to be '14', but got '{content}'"

def test_detect_script_exists():
    assert os.path.isfile(SCRIPT_FILE), f"Detection script missing at {SCRIPT_FILE}"

def test_adversarial_corpus():
    assert os.path.isfile(SCRIPT_FILE), f"Detection script missing at {SCRIPT_FILE}"

    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        result = subprocess.run(["python3", SCRIPT_FILE, evil_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            evil_bypassed.append(f"{os.path.basename(evil_file)} (output: {output})")

    for clean_file in clean_files:
        result = subprocess.run(["python3", SCRIPT_FILE, clean_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            clean_modified.append(f"{os.path.basename(clean_file)} (output: {output})")

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))