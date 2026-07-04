# test_final_state.py

import os
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
PIPELINE_GO = "/home/user/pipeline.go"

def run_detect(file_path):
    """Runs the Go program's detect subcommand on the given file."""
    cmd = ["go", "run", PIPELINE_GO, "detect", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip()

def test_pipeline_go_exists():
    assert os.path.exists(PIPELINE_GO), f"Missing Go program at {PIPELINE_GO}"
    assert os.path.isfile(PIPELINE_GO), f"{PIPELINE_GO} is not a file"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    assert clean_files, "Clean corpus is empty or missing."

    modified = []
    for filename in clean_files:
        file_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        rc, stdout = run_detect(file_path)
        if rc != 0 or stdout != "CLEAN":
            modified.append(filename)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (failed to print CLEAN and exit 0). Offending files: {', '.join(modified)}")

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    assert evil_files, "Evil corpus is empty or missing."

    bypassed = []
    for filename in evil_files:
        file_path = os.path.join(EVIL_CORPUS_DIR, filename)
        rc, stdout = run_detect(file_path)
        if rc != 1 or stdout != "EVIL":
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed (failed to print EVIL and exit 1). Offending files: {', '.join(bypassed)}")