# test_final_state.py
import os
import subprocess
import pytest

EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
SANITIZER_SCRIPT = "/app/sanitizer.py"
PYTHON_BIN = "/opt/venv/bin/python"

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_SCRIPT), f"{SANITIZER_SCRIPT} does not exist."

def test_adversarial_corpus():
    assert os.path.isfile(SANITIZER_SCRIPT), f"{SANITIZER_SCRIPT} does not exist."
    assert os.path.isfile(PYTHON_BIN), f"{PYTHON_BIN} does not exist."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([PYTHON_BIN, SANITIZER_SCRIPT, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_rejected = []
    for clean_file in clean_files:
        result = subprocess.run([PYTHON_BIN, SANITIZER_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")

    if errors:
        pytest.fail(" | ".join(errors))