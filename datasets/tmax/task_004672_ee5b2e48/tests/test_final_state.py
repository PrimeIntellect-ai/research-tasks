# test_final_state.py
import os
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLASSIFIER_SCRIPT = "/home/user/classifier.py"

def run_classifier(csv_path):
    assert os.path.exists(CLASSIFIER_SCRIPT), f"Classifier script not found at {CLASSIFIER_SCRIPT}"
    result = subprocess.run(
        ["python3", CLASSIFIER_SCRIPT, csv_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with exit code {result.returncode} for {csv_path}. Stderr: {result.stderr}"
    return result.stdout.strip()

def test_clean_corpus():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No clean CSV files found."

    failed_files = []
    for f in clean_files:
        path = os.path.join(CLEAN_CORPUS_DIR, f)
        output = run_classifier(path)
        if output != "CLEAN":
            failed_files.append((f, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(clean_files)} clean files rejected or invalid output.\n"
        for f, out in failed_files[:5]:
            error_msg += f"File: {f}, Output: {out}\n"
        pytest.fail(error_msg)

def test_evil_corpus():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No evil CSV files found."

    failed_files = []
    for f in evil_files:
        path = os.path.join(EVIL_CORPUS_DIR, f)
        output = run_classifier(path)
        if output != "EVIL":
            failed_files.append((f, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(evil_files)} evil files bypassed or invalid output.\n"
        for f, out in failed_files[:5]:
            error_msg += f"File: {f}, Output: {out}\n"
        pytest.fail(error_msg)