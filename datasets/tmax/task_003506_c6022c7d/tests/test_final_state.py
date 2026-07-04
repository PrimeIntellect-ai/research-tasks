# test_final_state.py
import os
import glob
import subprocess
import pytest

EVIL_DIR = "/app/corpora/evil"
CLEAN_DIR = "/app/corpora/clean"
SCRIPT_PATH = "/home/user/graph_sanitizer.py"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))
    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}"

    bypassed = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "REJECT":
            bypassed.append(os.path.basename(filepath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed}")

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}"

    rejected = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "ACCEPT":
            rejected.append(os.path.basename(filepath))

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(clean_files)} clean modified/rejected: {rejected}")