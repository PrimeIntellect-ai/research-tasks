# test_final_state.py

import os
import subprocess
import tempfile
import pytest

EXECUTABLE = "/home/user/log_organizer"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_executable_exists():
    """Ensure the Go program was compiled to the expected location."""
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_adversarial_corpus():
    """
    Test the agent's solution against both the clean and evil corpora.
    - Clean archives must be processed successfully and renamed.
    - Evil archives must be rejected and leave no files in the output directory.
    """
    clean_failed = []
    evil_failed = []

    # Ensure corpora directories exist
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing: {CLEAN_CORPUS}"
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing: {EVIL_CORPUS}"

    # Test clean corpus
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.tar.gz')]
    for cf in clean_files:
        in_path = os.path.join(CLEAN_CORPUS, cf)
        with tempfile.TemporaryDirectory() as out_dir:
            result = subprocess.run([EXECUTABLE, in_path, out_dir], capture_output=True, text=True)
            if result.returncode != 0:
                clean_failed.append(f"{cf} (rejected with exit code {result.returncode})")
                continue

            extracted = set(os.listdir(out_dir))
            if cf == "app_logs.tar.gz":
                expected = {"SECURELOG_web.txt", "SECURELOG_db.txt"}
                if not expected.issubset(extracted):
                    clean_failed.append(f"{cf} (missing expected renamed files, got {extracted})")

    # Test evil corpus
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.tar.gz')]
    for ef in evil_files:
        in_path = os.path.join(EVIL_CORPUS, ef)
        with tempfile.TemporaryDirectory() as out_dir:
            result = subprocess.run([EXECUTABLE, in_path, out_dir], capture_output=True, text=True)

            if result.returncode == 0:
                evil_failed.append(f"{ef} (exit code 0 - bypassed)")
                continue

            # Ensure nothing is left in the output directory
            extracted = os.listdir(out_dir)
            if len(extracted) > 0:
                evil_failed.append(f"{ef} (files written to out_dir despite being evil: {extracted})")

    # Surface a clear summary on failure
    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_failed))
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: " + ", ".join(clean_failed))

    assert not errors, " | ".join(errors)