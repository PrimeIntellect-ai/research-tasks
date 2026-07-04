# test_final_state.py

import os
import subprocess
import pytest

EVIL_CORPUS_PATH = "/app/corpus/evil"
CLEAN_CORPUS_PATH = "/app/corpus/clean"
DETECTOR_PATH = "/home/user/detector"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector binary {DETECTOR_PATH} does not exist."
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector binary {DETECTOR_PATH} is not executable."

def test_detector_against_corpus():
    # Setup environment to ensure the dynamic linker can find the shared library
    env = os.environ.copy()
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = "/app/libsecauth-1.0:" + env["LD_LIBRARY_PATH"]
    else:
        env["LD_LIBRARY_PATH"] = "/app/libsecauth-1.0"

    # Gather corpus files
    evil_files = [
        os.path.join(EVIL_CORPUS_PATH, f) for f in os.listdir(EVIL_CORPUS_PATH)
        if os.path.isfile(os.path.join(EVIL_CORPUS_PATH, f))
    ]
    clean_files = [
        os.path.join(CLEAN_CORPUS_PATH, f) for f in os.listdir(CLEAN_CORPUS_PATH)
        if os.path.isfile(os.path.join(CLEAN_CORPUS_PATH, f))
    ]

    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_PATH}."
    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_PATH}."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus (expected REJECT)
    for fpath in evil_files:
        result = subprocess.run(
            [DETECTOR_PATH, fpath],
            env=env,
            capture_output=True,
            text=True
        )
        if result.stdout.strip() != "REJECT":
            evil_bypassed.append(os.path.basename(fpath))

    # Test clean corpus (expected ACCEPT)
    for fpath in clean_files:
        result = subprocess.run(
            [DETECTOR_PATH, fpath],
            env=env,
            capture_output=True,
            text=True
        )
        if result.stdout.strip() != "ACCEPT":
            clean_modified.append(os.path.basename(fpath))

    # Summarize failures
    error_messages = []
    if evil_bypassed:
        error_messages.append(
            f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}"
        )
    if clean_modified:
        error_messages.append(
            f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}"
        )

    if error_messages:
        pytest.fail(" | ".join(error_messages))