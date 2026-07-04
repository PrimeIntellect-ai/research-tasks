# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.py"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_detector_script_exists():
    """Ensure the detector script was created."""
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

def test_adversarial_corpus():
    """Test the detector script against the evil and clean corpora."""
    assert os.path.isfile(DETECTOR_SCRIPT), "Detector script is missing."

    evil_files = []
    if os.path.isdir(EVIL_CORPUS_DIR):
        evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    clean_files = []
    if os.path.isdir(CLEAN_CORPUS_DIR):
        clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "Evil corpus is empty or missing."
    assert len(clean_files) > 0, "Clean corpus is empty or missing."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        try:
            result = subprocess.run(
                ["python3", DETECTOR_SCRIPT, evil_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "EVIL":
                evil_bypassed.append((os.path.basename(evil_file), output))
        except Exception as e:
            evil_bypassed.append((os.path.basename(evil_file), f"Error: {str(e)}"))

    for clean_file in clean_files:
        try:
            result = subprocess.run(
                ["python3", DETECTOR_SCRIPT, clean_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_modified.append((os.path.basename(clean_file), output))
        except Exception as e:
            clean_modified.append((os.path.basename(clean_file), f"Error: {str(e)}"))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join([f[0] for f in evil_bypassed])}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected). Offending files: {', '.join([f[0] for f in clean_modified])}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_messages)