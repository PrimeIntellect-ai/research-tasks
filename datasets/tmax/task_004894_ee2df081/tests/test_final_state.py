# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_CORPUS_DIR = "/app/corpora/evil/"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector executable not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector at {DETECTOR_PATH} is not executable"

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in evil corpus directory: {EVIL_CORPUS_DIR}"

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)

        # Run the detector
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/app/sdk:" + env.get("LD_LIBRARY_PATH", "")

        result = subprocess.run(
            [DETECTOR_PATH, filepath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env
        )

        # Exit code 1 (evil) or 2 (malformed) are acceptable for rejection
        if result.returncode not in (1, 2):
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")

def test_clean_corpus_accepted():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in clean corpus directory: {CLEAN_CORPUS_DIR}"

    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)

        # Run the detector
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/app/sdk:" + env.get("LD_LIBRARY_PATH", "")

        result = subprocess.run(
            [DETECTOR_PATH, filepath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env
        )

        # Exit code 0 (clean) is required
        if result.returncode != 0:
            modified_files.append(filename)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(modified_files)}")