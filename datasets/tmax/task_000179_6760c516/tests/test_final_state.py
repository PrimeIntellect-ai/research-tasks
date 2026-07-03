# test_final_state.py

import os
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/qemu_filter.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_filter_script_exists():
    assert os.path.isfile(FILTER_SCRIPT), f"Filter script not found at {FILTER_SCRIPT}"

def test_adversarial_corpus():
    assert os.path.isfile(FILTER_SCRIPT), f"Filter script not found at {FILTER_SCRIPT}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    failed_clean = []
    failed_evil = []

    for cf in clean_files:
        result = subprocess.run(["python3", FILTER_SCRIPT, cf], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run(["python3", FILTER_SCRIPT, ef], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_evil)}")

    if errors:
        pytest.fail(" | ".join(errors))