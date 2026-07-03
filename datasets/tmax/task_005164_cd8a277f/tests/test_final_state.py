# test_final_state.py

import os
import subprocess
import glob
import pytest

BINARY_PATH = "/home/user/sim_filter/target/release/sim_filter"
CLEAN_CORPUS = "/app/sim_corpus/clean"
EVIL_CORPUS = "/app/sim_corpus/evil"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Rust binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"File at {BINARY_PATH} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing: {CLEAN_CORPUS}"
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing: {EVIL_CORPUS}"

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS, "*.h5"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS, "*.h5"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([BINARY_PATH, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run([BINARY_PATH, ef], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    assert not errors, " | ".join(errors)