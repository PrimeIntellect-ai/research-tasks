# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/video_analyzer/target/release/payload_filter"
EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Expected binary not found at {BINARY_PATH}. Did you compile it in release mode?"
    assert os.access(BINARY_PATH, os.X_OK), f"The file at {BINARY_PATH} is not executable."

def test_payload_filter_behavior():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]

    assert evil_files, "No JSON files found in evil corpus."
    assert clean_files, "No JSON files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        try:
            result = subprocess.run(
                [BINARY_PATH, evil_file],
                capture_output=True,
                timeout=5  # Prevent infinite loops
            )
            if result.returncode == 0:
                evil_bypassed.append(os.path.basename(evil_file))
        except subprocess.TimeoutExpired:
            # Timeout is considered a failure since the requirement says it must not hang infinitely
            evil_bypassed.append(f"{os.path.basename(evil_file)} (timeout)")
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(evil_file)} (error: {str(e)})")

    # Test clean corpus
    for clean_file in clean_files:
        try:
            result = subprocess.run(
                [BINARY_PATH, clean_file],
                capture_output=True,
                timeout=5
            )
            if result.returncode != 0:
                clean_modified.append(os.path.basename(clean_file))
        except subprocess.TimeoutExpired:
            clean_modified.append(f"{os.path.basename(clean_file)} (timeout)")
        except Exception as e:
            clean_modified.append(f"{os.path.basename(clean_file)} (error: {str(e)})")

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean rejected: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_messages)