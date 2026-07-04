# test_final_state.py
import os
import subprocess
import pytest

CLEAN_CORPUS = "/home/user/manifests/clean/"
EVIL_CORPUS = "/home/user/manifests/evil/"
SCRIPT_PATH = "/home/user/pipeline_guard.py"

def test_pipeline_guard_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus missing: {CLEAN_CORPUS}"
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus missing: {EVIL_CORPUS}"

    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]

    assert len(clean_files) > 0, "No files in clean corpus."
    assert len(evil_files) > 0, "No files in evil corpus."

    failed_clean = []
    failed_evil = []

    for f in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(f))

    for f in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(f))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_evil)}")

    if errors:
        pytest.fail(" | ".join(errors))