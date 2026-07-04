# test_final_state.py
import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.sh"
EVIL_CORPUS_DIR = "/app/corpora/evil/"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script {DETECTOR_SCRIPT} does not exist."
    assert os.access(DETECTOR_SCRIPT, os.X_OK), f"Detector script {DETECTOR_SCRIPT} is not executable."

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    evil_files = sorted([
        os.path.join(EVIL_CORPUS_DIR, f) 
        for f in os.listdir(EVIL_CORPUS_DIR) 
        if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))
    ])
    clean_files = sorted([
        os.path.join(CLEAN_CORPUS_DIR, f) 
        for f in os.listdir(CLEAN_CORPUS_DIR) 
        if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))
    ])

    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    evil_bypassed = []
    for f in evil_files:
        try:
            result = subprocess.run([DETECTOR_SCRIPT, f], capture_output=True, text=True, timeout=2)
            if result.stdout.strip() != "EVIL":
                evil_bypassed.append(os.path.basename(f))
        except Exception:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        try:
            result = subprocess.run([DETECTOR_SCRIPT, f], capture_output=True, text=True, timeout=2)
            if result.stdout.strip() != "CLEAN":
                clean_modified.append(os.path.basename(f))
        except Exception:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        offending = ", ".join(evil_bypassed[:10]) + ("..." if len(evil_bypassed) > 10 else "")
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: {offending}")

    if clean_modified:
        offending = ", ".join(clean_modified[:10]) + ("..." if len(clean_modified) > 10 else "")
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified. Offending files: {offending}")

    if errors:
        pytest.fail(" | ".join(errors))