# test_final_state.py
import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
CLEAN_CORPUS_PATH = "/app/corpus/clean"
EVIL_CORPUS_PATH = "/app/corpus/evil"

def test_detector_executable_exists():
    assert os.path.isfile(DETECTOR_PATH), f"Detector executable missing at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector at {DETECTOR_PATH} is not executable"

def test_adversarial_corpus():
    if not os.path.isfile(DETECTOR_PATH) or not os.access(DETECTOR_PATH, os.X_OK):
        pytest.fail(f"Detector executable not found or not executable at {DETECTOR_PATH}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_PATH) if f.endswith('.wav')]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_PATH) if f.endswith('.wav')]

    assert len(clean_files) > 0, f"No WAV files found in {CLEAN_CORPUS_PATH}"
    assert len(evil_files) > 0, f"No WAV files found in {EVIL_CORPUS_PATH}"

    clean_modified = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_PATH, f)
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(f)

    evil_bypassed = []
    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS_PATH, f)
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))