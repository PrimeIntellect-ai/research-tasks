# test_final_state.py

import os
import subprocess
import pytest

FILTER_SCRIPT = '/home/user/filter.py'
EVIL_CORPUS_DIR = '/app/eval_corpus/evil'
CLEAN_CORPUS_DIR = '/app/eval_corpus/clean'

def test_filter_script_exists():
    assert os.path.isfile(FILTER_SCRIPT), f"The filter script {FILTER_SCRIPT} is missing."

def test_adversarial_corpus_filtering():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing."
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "No evil files found in the corpus."
    assert len(clean_files) > 0, "No clean files found in the corpus."

    bypassed_evil = []
    for evil_file in evil_files:
        result = subprocess.run(['python3', FILTER_SCRIPT, evil_file], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append((os.path.basename(evil_file), result.returncode))

    modified_clean = []
    for clean_file in clean_files:
        result = subprocess.run(['python3', FILTER_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            modified_clean.append((os.path.basename(clean_file), result.returncode))

    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed the filter. Offending files: " + ", ".join([f"{f} (exit code {c})" for f, c in bypassed_evil]))

    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean files were incorrectly flagged. Offending files: " + ", ".join([f"{f} (exit code {c})" for f, c in modified_clean]))

    assert not error_messages, "\n".join(error_messages)