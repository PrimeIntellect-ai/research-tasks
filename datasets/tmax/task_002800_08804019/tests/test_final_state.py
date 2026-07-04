# test_final_state.py

import os
import subprocess
import pytest

DETECT_SCRIPT = "/home/user/detect.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_detect_script_exists_and_executable():
    assert os.path.isfile(DETECT_SCRIPT), f"The script {DETECT_SCRIPT} does not exist."
    assert os.access(DETECT_SCRIPT, os.X_OK), f"The script {DETECT_SCRIPT} is not executable."

def test_adversarial_corpus():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}."
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([DETECT_SCRIPT, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run([DETECT_SCRIPT, ef], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    assert not errors, "Adversarial corpus validation failed:\n" + "\n".join(errors)