# test_final_state.py

import os
import subprocess
import glob
import pytest

EVIL_DIR = "/app/corpora/evil"
CLEAN_DIR = "/app/corpora/clean"
SCRIPT_PATH = "/home/user/classifier.py"
C_FILE_PATH = "/app/vendored_parser/src/parser.c"

def test_classifier_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Classifier script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_c_extension_fixed():
    assert os.path.exists(C_FILE_PATH), f"C file not found at {C_FILE_PATH}"
    with open(C_FILE_PATH, "r") as f:
        content = f.read()
        assert "(float)" not in content, "The C extension still contains the intentional `(float)` cast bug causing precision loss."

def test_adversarial_corpus():
    evil_files = sorted(glob.glob(os.path.join(EVIL_DIR, "*.pcap")))
    clean_files = sorted(glob.glob(os.path.join(CLEAN_DIR, "*.pcap")))

    assert len(evil_files) > 0, f"No pcap files found in {EVIL_DIR}"
    assert len(clean_files) > 0, f"No pcap files found in {CLEAN_DIR}"

    # Run the classifier on the evil directory
    result_evil = subprocess.run(
        ["python3", SCRIPT_PATH, EVIL_DIR],
        capture_output=True,
        text=True
    )
    assert result_evil.returncode == 0, f"Classifier script failed on evil corpus:\n{result_evil.stderr}"

    # Run the classifier on the clean directory
    result_clean = subprocess.run(
        ["python3", SCRIPT_PATH, CLEAN_DIR],
        capture_output=True,
        text=True
    )
    assert result_clean.returncode == 0, f"Classifier script failed on clean corpus:\n{result_clean.stderr}"

    evil_output = result_evil.stdout.strip().splitlines()
    clean_output = result_clean.stdout.strip().splitlines()

    evil_bypassed = []
    for pcap in evil_files:
        basename = os.path.basename(pcap)
        expected = f"{basename}: EVIL"
        if expected not in evil_output:
            evil_bypassed.append(basename)

    clean_modified = []
    for pcap in clean_files:
        basename = os.path.basename(pcap)
        expected = f"{basename}: CLEAN"
        if expected not in clean_output:
            clean_modified.append(basename)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)