# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/telemetry_classifier/bin/classifier"
EVIL_CORPUS_DIR = "/app/corpora/evil/"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"

def test_binary_exists_and_executable():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}. Did the build script succeed?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable."

def test_classifier_accuracy():
    assert os.path.isfile(BINARY_PATH), "Binary missing, cannot test accuracy."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    evil_bypassed = []
    clean_modified = []

    # Test EVIL corpus
    for filepath in evil_files:
        try:
            result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "EVIL":
                evil_bypassed.append(os.path.basename(filepath))
        except subprocess.TimeoutExpired:
            evil_bypassed.append(f"{os.path.basename(filepath)} (timeout)")
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(filepath)} (error: {e})")

    # Test CLEAN corpus
    for filepath in clean_files:
        try:
            result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_modified.append(os.path.basename(filepath))
        except subprocess.TimeoutExpired:
            clean_modified.append(f"{os.path.basename(filepath)} (timeout)")
        except Exception as e:
            clean_modified.append(f"{os.path.basename(filepath)} (error: {e})")

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:10])}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified[:10])}")

    assert not evil_bypassed and not clean_modified, "Classifier accuracy failed:\n" + "\n".join(error_messages)