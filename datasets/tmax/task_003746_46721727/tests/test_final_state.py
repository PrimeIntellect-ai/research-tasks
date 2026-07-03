# test_final_state.py

import os
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/classifier.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def run_classifier(file_path):
    result = subprocess.run(
        ["python3", AGENT_SCRIPT, file_path],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.stdout.strip()

def test_classifier_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert clean_files, "No clean corpus files found."

    failed_files = []
    for filepath in clean_files:
        output = run_classifier(filepath)
        if output != "CLEAN":
            failed_files.append((os.path.basename(filepath), output))

    if failed_files:
        details = ", ".join([f"{f} (got '{o}')" for f, o in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected incorrectly: {details}")

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert evil_files, "No evil corpus files found."

    failed_files = []
    for filepath in evil_files:
        output = run_classifier(filepath)
        if output != "EVIL":
            failed_files.append((os.path.basename(filepath), output))

    if failed_files:
        details = ", ".join([f"{f} (got '{o}')" for f, o in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed incorrectly: {details}")