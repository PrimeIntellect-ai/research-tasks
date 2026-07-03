# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/classify.sh"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK) or os.access(SCRIPT_PATH, os.R_OK), f"Script {SCRIPT_PATH} cannot be read/executed."

def test_hidden_corpus_classification():
    hidden_clean_dir = "/app/hidden_corpus/clean"
    hidden_evil_dir = "/app/hidden_corpus/evil"

    clean_files = glob.glob(os.path.join(hidden_clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(hidden_evil_dir, "*.csv"))

    assert len(clean_files) > 0, f"No clean files found in {hidden_clean_dir}."
    assert len(evil_files) > 0, f"No evil files found in {hidden_evil_dir}."

    clean_failed = []
    evil_failed = []

    # Check clean corpus
    for f in clean_files:
        result = subprocess.run(["bash", SCRIPT_PATH, f], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            clean_failed.append(os.path.basename(f))

    # Check evil corpus
    for f in evil_files:
        result = subprocess.run(["bash", SCRIPT_PATH, f], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            evil_failed.append(os.path.basename(f))

    error_messages = []
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    assert not error_messages, " | ".join(error_messages)