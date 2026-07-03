# test_final_state.py

import os
import subprocess
import pytest

CLASSIFIER_SCRIPT = "/home/user/patch_classifier.py"
EVIL_CORPUS_DIR = "/var/opt/verifier/corpora/evil/"
CLEAN_CORPUS_DIR = "/var/opt/verifier/corpora/clean/"

def run_classifier(file_path):
    try:
        result = subprocess.run(
            ["python3", CLASSIFIER_SCRIPT, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return result.returncode, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -2, str(e)

def test_classifier_script_exists():
    assert os.path.exists(CLASSIFIER_SCRIPT), f"Classifier script not found at {CLASSIFIER_SCRIPT}"
    assert os.path.isfile(CLASSIFIER_SCRIPT), f"{CLASSIFIER_SCRIPT} is not a file"

def test_evil_corpus_rejected():
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "Evil corpus is empty."

    failures = []
    for filepath in evil_files:
        basename = os.path.basename(filepath)
        returncode, stdout = run_classifier(filepath)
        if returncode != 1 or stdout != "EVIL":
            failures.append(f"{basename} (code: {returncode}, out: {stdout})")

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil bypassed: " + ", ".join(failures))

def test_clean_corpus_accepted():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "Clean corpus is empty."

    failures = []
    for filepath in clean_files:
        basename = os.path.basename(filepath)
        returncode, stdout = run_classifier(filepath)
        if returncode != 0 or stdout != "CLEAN":
            failures.append(f"{basename} (code: {returncode}, out: {stdout})")

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean modified/rejected: " + ", ".join(failures))