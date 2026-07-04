# test_final_state.py

import os
import subprocess
import pytest

CLEAN_DIR = "/app/corpora/clean/"
EVIL_DIR = "/app/corpora/evil/"
GO_SCRIPT = "/home/user/detect_anomaly.go"

def test_go_script_exists():
    assert os.path.isfile(GO_SCRIPT), f"Go script not found at {GO_SCRIPT}"

def test_adversarial_corpus():
    assert os.path.isfile(GO_SCRIPT), f"Go script not found at {GO_SCRIPT}"

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.tsv')]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.tsv')]

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run(["go", "run", GO_SCRIPT, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run(["go", "run", GO_SCRIPT, ef], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    errors = []
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")

    if errors:
        pytest.fail(" | ".join(errors))