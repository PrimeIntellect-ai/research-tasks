# test_final_state.py

import os
import subprocess
import pytest

def test_classifier_exists():
    assert os.path.isfile("/home/user/classifier"), "/home/user/classifier executable is missing"
    assert os.access("/home/user/classifier", os.X_OK), "/home/user/classifier is not executable"

def test_adversarial_corpus():
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"
    executable = "/home/user/classifier"

    assert os.path.isdir(clean_dir), f"{clean_dir} directory is missing"
    assert os.path.isdir(evil_dir), f"{evil_dir} directory is missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    failed_clean = []
    failed_evil = []

    for cf in clean_files:
        result = subprocess.run([executable, cf], capture_output=True, text=True)
        if result.stdout.strip() != "CLEAN":
            failed_clean.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([executable, ef], capture_output=True, text=True)
        if result.stdout.strip() != "EVIL":
            failed_evil.append(os.path.basename(ef))

    errors = []
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified: {', '.join(failed_clean)}")

    assert not errors, " | ".join(errors)