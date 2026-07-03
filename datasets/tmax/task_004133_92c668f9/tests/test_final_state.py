# test_final_state.py

import os
import stat
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/filter.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_filter_script_exists_and_executable():
    assert os.path.isfile(FILTER_SCRIPT), f"Filter script not found at {FILTER_SCRIPT}"
    st = os.stat(FILTER_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Filter script {FILTER_SCRIPT} is not executable"

def test_adversarial_corpus_verification():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "No files found in clean corpus"
    assert len(evil_files) > 0, "No files found in evil corpus"

    clean_failed = []
    evil_failed = []

    for clean_file in clean_files:
        result = subprocess.run([FILTER_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        result = subprocess.run([FILTER_SCRIPT, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(evil_file))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(clean_failed[:10])}{'...' if len(clean_failed) > 10 else ''}")

    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(evil_failed[:10])}{'...' if len(evil_failed) > 10 else ''}")

    assert not error_messages, " | ".join(error_messages)