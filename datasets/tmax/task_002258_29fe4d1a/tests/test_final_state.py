# test_final_state.py

import os
import glob
import subprocess
from pathlib import Path

def test_detector_script_exists():
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Detector script is missing at {detector_path}"

def test_adversarial_corpus():
    detector_path = "/home/user/detector.py"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    clean_failed = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", detector_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(clean_file))

    evil_failed = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", detector_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(evil_file))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    assert not errors, " | ".join(errors)