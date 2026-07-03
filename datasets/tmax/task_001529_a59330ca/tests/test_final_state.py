# test_final_state.py

import os
import re
import subprocess
import pytest

BINARY_PATH = "/home/user/audio-detector"
TRANSCRIPT_PATH = "/home/user/transcript.txt"
EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EXPECTED_TRANSCRIPT = "PROJECT OVERSEER HAS BEEN COMPROMISED WE NEED IMMEDIATE EVACUATION"

def test_binary_exists_and_executable():
    """Test that the compiled binary exists and is executable."""
    assert os.path.isfile(BINARY_PATH), f"Expected binary {BINARY_PATH} does not exist."
    assert os.access(BINARY_PATH, os.X_OK), f"Binary {BINARY_PATH} is not executable."

def test_transcript_content():
    """Test that the transcript file exists and contains the correct text."""
    assert os.path.isfile(TRANSCRIPT_PATH), f"Expected transcript file {TRANSCRIPT_PATH} does not exist."

    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean up both expected and actual text: uppercase, remove non-alphanumeric chars
    clean_content = re.sub(r'[^A-Z0-9]', '', content.upper())
    clean_expected = re.sub(r'[^A-Z0-9]', '', EXPECTED_TRANSCRIPT.upper())

    assert clean_expected in clean_content, f"Transcript does not contain the expected text. Found: {content.strip()}"

def test_adversarial_corpus():
    """Test that the binary correctly classifies clean and evil audio files."""
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus dir {EVIL_CORPUS_DIR} missing."
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus dir {CLEAN_CORPUS_DIR} missing."

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.wav')]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.wav')]

    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}."
    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}."

    evil_bypassed = []
    for f in evil_files:
        path = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run([BINARY_PATH, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 1:
            evil_bypassed.append(f)

    clean_modified = []
    for f in clean_files:
        path = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run([BINARY_PATH, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)