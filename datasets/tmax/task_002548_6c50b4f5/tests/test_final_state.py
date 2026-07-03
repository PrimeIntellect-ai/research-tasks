# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detector.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_detector_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The required script was not found at {SCRIPT_PATH}"

def test_adversarial_corpus():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.wav"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.wav"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    failed_clean = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(clean_file))

    failed_evil = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, evil_file], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(evil_file))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean files modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed: {', '.join(failed_evil)}")

    assert not errors, "Adversarial corpus validation failed:\n" + "\n".join(errors)