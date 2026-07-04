# test_final_state.py

import os
import subprocess
import glob
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector executable not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector at {DETECTOR_PATH} is not executable"

def test_adversarial_corpus():
    if not os.path.isfile(DETECTOR_PATH) or not os.access(DETECTOR_PATH, os.X_OK):
        pytest.fail("Detector is missing or not executable; cannot run corpus tests.")

    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.mp4"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.mp4"))

    if not evil_files:
        pytest.fail(f"No MP4 files found in evil corpus dir: {EVIL_CORPUS_DIR}")
    if not clean_files:
        pytest.fail(f"No MP4 files found in clean corpus dir: {CLEAN_CORPUS_DIR}")

    evil_bypassed = []
    clean_modified = []

    for ef in evil_files:
        try:
            result = subprocess.run([DETECTOR_PATH, ef], capture_output=True, text=True, timeout=15)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_bypassed.append((os.path.basename(ef), output))
        except Exception as e:
            evil_bypassed.append((os.path.basename(ef), f"Error: {e}"))

    for cf in clean_files:
        try:
            result = subprocess.run([DETECTOR_PATH, cf], capture_output=True, text=True, timeout=15)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_modified.append((os.path.basename(cf), output))
        except Exception as e:
            clean_modified.append((os.path.basename(cf), f"Error: {e}"))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: " + ", ".join([f"{f} (Output: {out})" for f, out in evil_bypassed[:5]]) + ("..." if len(evil_bypassed) > 5 else ""))

    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected). Offending files: " + ", ".join([f"{f} (Output: {out})" for f, out in clean_modified[:5]]) + ("..." if len(clean_modified) > 5 else ""))

    if error_messages:
        pytest.fail(" | ".join(error_messages))