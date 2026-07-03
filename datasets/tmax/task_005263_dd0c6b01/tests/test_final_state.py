# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/audit_classifier.sh"
EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"The path {SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"The script {SCRIPT_PATH} is not executable."

def run_classifier(file_path):
    try:
        result = subprocess.run(
            [SCRIPT_PATH, file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def test_adversarial_corpus():
    # Gather files
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, f"No files found in evil corpus directory: {EVIL_CORPUS_DIR}"
    assert len(clean_files) > 0, f"No files found in clean corpus directory: {CLEAN_CORPUS_DIR}"

    bypassed_evil = []
    modified_clean = []

    # Test evil corpus
    for evil_file in evil_files:
        output = run_classifier(evil_file)
        if output != "EVIL\n":
            bypassed_evil.append((os.path.basename(evil_file), output.strip()))

    # Test clean corpus
    for clean_file in clean_files:
        output = run_classifier(clean_file)
        if output != "CLEAN\n":
            modified_clean.append((os.path.basename(clean_file), output.strip()))

    # Summarize failures
    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed:")
        for f, out in bypassed_evil:
            error_messages.append(f"  - {f} (Output: {repr(out)})")

    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified/rejected:")
        for f, out in modified_clean:
            error_messages.append(f"  - {f} (Output: {repr(out)})")

    if error_messages:
        pytest.fail("\n".join(error_messages))