# test_final_state.py

import os
import subprocess
import pytest
from pathlib import Path

DETECTOR_SCRIPT = "/home/user/detector.py"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_detector_script_exists():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

def run_detector(filepath):
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, str(filepath)],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.stdout.strip()

def test_evil_corpus():
    evil_files = list(Path(EVIL_CORPUS_DIR).glob("*.json"))
    assert len(evil_files) > 0, f"No json files found in {EVIL_CORPUS_DIR}"

    bypassed = []
    for filepath in evil_files:
        output = run_detector(filepath)
        if output != "EVIL":
            bypassed.append((filepath.name, output))

    if bypassed:
        details = ", ".join([f"{f} (output: {o})" for f, o in bypassed])
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {details}")

def test_clean_corpus():
    clean_files = list(Path(CLEAN_CORPUS_DIR).glob("*.json"))
    assert len(clean_files) > 0, f"No json files found in {CLEAN_CORPUS_DIR}"

    modified = []
    for filepath in clean_files:
        output = run_detector(filepath)
        if output != "CLEAN":
            modified.append((filepath.name, output))

    if modified:
        details = ", ".join([f"{f} (output: {o})" for f, o in modified])
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/flagged. Offending files: {details}")