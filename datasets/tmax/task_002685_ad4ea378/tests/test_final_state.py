# test_final_state.py

import os
import glob
import subprocess

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable missing: {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector is not executable: {detector_path}"

def test_adversarial_corpus():
    detector_path = "/home/user/detector"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.pgm"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.pgm"))

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run([detector_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run([detector_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected (expected exit code 0): {clean_failures}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (expected exit code 1): {evil_failures}")

    assert not error_msg, " | ".join(error_msg)

def test_clean_count():
    count_file = "/home/user/clean_count.txt"
    assert os.path.isfile(count_file), f"Count file missing: {count_file}"

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Count file does not contain a valid integer: '{content}'"
    count = int(content)

    assert count == 45, f"Expected clean count to be 45, but got {count}"