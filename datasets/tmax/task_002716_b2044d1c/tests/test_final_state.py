# test_final_state.py
import os
import subprocess
import pytest

CLASSIFIER_BIN = "/home/user/qa-env/wsprocessor/bin/classifier"
CLEAN_CORPUS_DIR = "/home/user/corpora/clean"
EVIL_CORPUS_DIR = "/home/user/corpora/evil"

def test_classifier_binary_exists():
    assert os.path.isfile(CLASSIFIER_BIN), f"Classifier binary not found at {CLASSIFIER_BIN}"
    assert os.access(CLASSIFIER_BIN, os.X_OK), f"Classifier binary at {CLASSIFIER_BIN} is not executable"

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(files) > 0, "Clean corpus is empty."

    modified_files = []
    for f in files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, f)
        try:
            result = subprocess.run([CLASSIFIER_BIN, filepath], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "CLEAN":
                modified_files.append(f)
        except Exception as e:
            modified_files.append(f)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(files)} clean modified/rejected. Offending files: {', '.join(modified_files)}")

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(files) > 0, "Evil corpus is empty."

    bypassed_files = []
    for f in files:
        filepath = os.path.join(EVIL_CORPUS_DIR, f)
        try:
            result = subprocess.run([CLASSIFIER_BIN, filepath], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "EVIL":
                bypassed_files.append(f)
        except Exception as e:
            bypassed_files.append(f)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")

def test_go_build_success():
    # Test that the project builds without circular import errors
    ws_dir = "/home/user/qa-env/wsprocessor"
    try:
        result = subprocess.run(["go", "build", "./..."], cwd=ws_dir, capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"go build failed: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to run go build: {e}")