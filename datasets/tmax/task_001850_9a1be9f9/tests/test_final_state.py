# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"

def test_detector_script_exists():
    assert os.path.exists(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"
    assert os.path.isfile(DETECTOR_SCRIPT), f"{DETECTOR_SCRIPT} is not a file"

def test_clean_corpus_preserved():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["python3", DETECTOR_SCRIPT, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean logs were incorrectly rejected (exit code != 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["python3", DETECTOR_SCRIPT, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil logs bypassed the detector (exit code != 1). Offending files: {', '.join(failed_files)}")