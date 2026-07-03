# test_final_state.py

import os
import subprocess
import pytest

EVIL_DIR = "/app/corpora/evil/"
CLEAN_DIR = "/app/corpora/clean/"
SCRIPT_PATH = "/home/user/classify_hog.py"

def run_script(input_data):
    """Helper to run the student script with given standard input."""
    result = subprocess.run(
        [SCRIPT_PATH],
        input=input_data.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    return result.stdout.decode('utf-8').strip()

def test_script_exists_and_executable():
    """Check that the classification script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_evil_corpus_rejected():
    """Ensure all evil inputs (exceeding limits and not ignored) are REJECTED."""
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"

    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, "Evil corpus is empty"

    bypassed = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        try:
            output = run_script(content)
            if output != "REJECT":
                bypassed.append(filename)
        except Exception as e:
            bypassed.append(f"{filename} (Error: {str(e)})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_clean_corpus_accepted():
    """Ensure all clean inputs (within limits or matching ignore path) are ACCEPTED."""
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "Clean corpus is empty"

    modified = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        try:
            output = run_script(content)
            if output != "ACCEPT":
                modified.append(filename)
        except Exception as e:
            modified.append(f"{filename} (Error: {str(e)})")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(modified)}")