# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_submission.py"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Missing classifier script: {SCRIPT_PATH}"

def run_classifier(file_path):
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_clean_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Missing clean corpus directory: {CLEAN_DIR}"
    clean_files = sorted([f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')])
    assert len(clean_files) > 0, "No JSON files found in clean corpus"

    failed_files = []

    for f in clean_files:
        file_path = os.path.join(CLEAN_DIR, f)
        output = run_classifier(file_path)
        if output != "ACCEPT":
            failed_files.append((f, output))

    if failed_files:
        msg = f"{len(failed_files)} of {len(clean_files)} clean modified (rejected or errored).\nOffending files:\n"
        for f, out in failed_files:
            msg += f"  {f} (output: {out})\n"
        pytest.fail(msg)

def test_evil_corpus():
    assert os.path.isdir(EVIL_DIR), f"Missing evil corpus directory: {EVIL_DIR}"
    evil_files = sorted([f for f in os.listdir(EVIL_DIR) if f.endswith('.json')])
    assert len(evil_files) > 0, "No JSON files found in evil corpus"

    failed_files = []

    for f in evil_files:
        file_path = os.path.join(EVIL_DIR, f)
        output = run_classifier(file_path)
        if output != "REJECT":
            failed_files.append((f, output))

    if failed_files:
        msg = f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted or errored).\nOffending files:\n"
        for f, out in failed_files:
            msg += f"  {f} (output: {out})\n"
        pytest.fail(msg)