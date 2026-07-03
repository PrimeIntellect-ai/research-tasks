# test_final_state.py

import os
import subprocess
import pytest

CLASSIFIER_PATH = "/home/user/classifier"
CLEAN_CORPUS_DIR = "/var/test_corpus/clean"
EVIL_CORPUS_DIR = "/var/test_corpus/evil"

def test_classifier_exists_and_executable():
    assert os.path.exists(CLASSIFIER_PATH), f"Classifier script not found at {CLASSIFIER_PATH}"
    assert os.path.isfile(CLASSIFIER_PATH), f"{CLASSIFIER_PATH} is not a file"
    assert os.access(CLASSIFIER_PATH, os.X_OK), f"Classifier script at {CLASSIFIER_PATH} is not executable"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "Clean corpus is empty"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        try:
            result = subprocess.run([CLASSIFIER_PATH, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "CLEAN":
                failed_files.append((filename, output))
        except Exception as e:
            failed_files.append((filename, str(e)))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(clean_files)} clean files failed (were not classified as CLEAN).\n"
        error_msg += "Offending files:\n"
        for f, out in failed_files[:10]:
            error_msg += f"  {f}: output '{out}'\n"
        if len(failed_files) > 10:
            error_msg += "  ...\n"
        pytest.fail(error_msg)

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "Evil corpus is empty"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        try:
            result = subprocess.run([CLASSIFIER_PATH, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "EVIL":
                failed_files.append((filename, output))
        except Exception as e:
            failed_files.append((filename, str(e)))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(evil_files)} evil files bypassed (were not classified as EVIL).\n"
        error_msg += "Offending files:\n"
        for f, out in failed_files[:10]:
            error_msg += f"  {f}: output '{out}'\n"
        if len(failed_files) > 10:
            error_msg += "  ...\n"
        pytest.fail(error_msg)