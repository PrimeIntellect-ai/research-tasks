# test_final_state.py

import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/check_tar.sh"
THUMBNAIL_PATH = "/home/user/thumbnail.jpg"
EVIL_CORPUS_DIR = "/app/corpora/evil/"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.tar"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.tar"))

    assert len(evil_files) > 0, "No evil corpus files found to test against."
    assert len(clean_files) > 0, "No clean corpus files found to test against."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["bash", SCRIPT_PATH, evil_file], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "REJECT":
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run(["bash", SCRIPT_PATH, clean_file], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "ACCEPT":
            clean_modified.append(os.path.basename(clean_file))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msg)

def test_thumbnail_extracted():
    assert os.path.isfile(THUMBNAIL_PATH), f"Thumbnail not found at {THUMBNAIL_PATH}"

    # Check if it's a valid JPEG
    with open(THUMBNAIL_PATH, "rb") as f:
        header = f.read(3)
        assert header == b'\xff\xd8\xff', f"File at {THUMBNAIL_PATH} is not a valid JPEG"

    # Check file size is reasonable
    size = os.path.getsize(THUMBNAIL_PATH)
    assert size > 1000, f"Thumbnail size ({size} bytes) is suspiciously small"