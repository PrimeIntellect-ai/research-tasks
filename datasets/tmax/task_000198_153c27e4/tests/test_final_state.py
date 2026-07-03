# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.exists(detector_path), f"Missing detector executable at {detector_path}"
    assert os.path.isfile(detector_path), f"{detector_path} is not a file"
    assert os.access(detector_path, os.X_OK), f"{detector_path} is not executable"

def test_detector_adversarial_corpus():
    detector_path = "/home/user/detector"
    evil_dir = "/app/test_corpus/evil"
    clean_dir = "/app/test_corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.nc"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.nc"))

    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"
    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"

    evil_bypassed = []
    for f in evil_files:
        try:
            result = subprocess.run([detector_path, f], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_bypassed.append(os.path.basename(f))
        except Exception as e:
            evil_bypassed.append(os.path.basename(f) + f" (Error: {e})")

    clean_rejected = []
    for f in clean_files:
        try:
            result = subprocess.run([detector_path, f], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_rejected.append(os.path.basename(f))
        except Exception as e:
            clean_rejected.append(os.path.basename(f) + f" (Error: {e})")

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_rejected)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))