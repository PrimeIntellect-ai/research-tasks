# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_CORPUS_DIR = "/opt/corpus/evil"
CLEAN_CORPUS_DIR = "/opt/corpus/clean"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Executable not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"File at {DETECTOR_PATH} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([DETECTOR_PATH, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_rejected = []
    for clean_file in clean_files:
        result = subprocess.run([DETECTOR_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}{'...' if len(evil_bypassed) > 5 else ''}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected[:5])}{'...' if len(clean_rejected) > 5 else ''}")

    assert not evil_bypassed and not clean_rejected, " | ".join(error_messages)