# test_final_state.py
import os
import subprocess
import glob
import pytest

EXECUTABLE = "/home/user/audit_checker"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_adversarial_corpus_evaluation():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for filepath in evil_files:
        try:
            result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "EVIL":
                evil_bypassed.append((os.path.basename(filepath), output))
        except Exception as e:
            evil_bypassed.append((os.path.basename(filepath), str(e)))

    clean_modified = []
    for filepath in clean_files:
        try:
            result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_modified.append((os.path.basename(filepath), output))
        except Exception as e:
            clean_modified.append((os.path.basename(filepath), str(e)))

    error_messages = []
    if evil_bypassed:
        basenames = [f[0] for f in evil_bypassed]
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(basenames)}")

    if clean_modified:
        basenames = [f[0] for f in clean_modified]
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(basenames)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))