# test_final_state.py

import os
import glob
import subprocess
import string
import pytest

BINARY_PATH = "/home/user/wav_filter/target/debug/wav_filter"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
TRANSCRIPT_PATH = "/home/user/transcript.txt"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Binary not found at {BINARY_PATH}. Did you compile the project?"
    assert os.access(BINARY_PATH, os.X_OK), f"File at {BINARY_PATH} is not executable."

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.wav"))
    assert len(evil_files) > 0, f"No evil WAV files found in {EVIL_CORPUS_DIR}"

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(filepath))

    assert len(bypassed_files) == 0, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed detection: {', '.join(bypassed_files)}"

def test_clean_corpus_preserved():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.wav"))
    assert len(clean_files) > 0, f"No clean WAV files found in {CLEAN_CORPUS_DIR}"

    modified_files = []
    for filepath in clean_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            modified_files.append(os.path.basename(filepath))

    assert len(modified_files) == 0, f"{len(modified_files)} of {len(clean_files)} clean files were incorrectly rejected: {', '.join(modified_files)}"

def test_transcript_content():
    assert os.path.isfile(TRANSCRIPT_PATH), f"Transcript file not found at {TRANSCRIPT_PATH}"

    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        content = f.read().lower()

    # Remove punctuation
    content_clean = content.translate(str.maketrans('', '', string.punctuation)).strip()

    expected_phrase = "deploy the countermeasures"
    assert expected_phrase in content_clean, f"Transcript does not contain the expected phrase. Found: {content_clean}"