# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.py"
CLEAN_CORPUS_DIR = "/app/data/clean"
EVIL_CORPUS_DIR = "/app/data/evil"

def test_detector_script_exists():
    assert os.path.exists(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"
    assert os.path.isfile(DETECTOR_SCRIPT), f"{DETECTOR_SCRIPT} is not a file"

def run_detector(filepath):
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.returncode, result.stdout.strip()

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory not found at {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"

    bypassed_files = []

    for filepath in evil_files:
        returncode, stdout = run_detector(filepath)
        if returncode != 1 or stdout != "EVIL":
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed detection. Offending files: {', '.join(bypassed_files)}")

def test_clean_corpus_preserved():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory not found at {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    modified_files = []

    for filepath in clean_files:
        returncode, stdout = run_detector(filepath)
        if returncode != 0 or stdout != "CLEAN":
            modified_files.append(os.path.basename(filepath))

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean files were incorrectly flagged as evil. Offending files: {', '.join(modified_files)}")