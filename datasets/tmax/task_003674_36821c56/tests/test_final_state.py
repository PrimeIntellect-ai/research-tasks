# test_final_state.py
import os
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
WRAPPER_SCRIPT = "/home/user/test_waf.sh"

def test_wrapper_script_exists_and_executable():
    assert os.path.isfile(WRAPPER_SCRIPT), f"Wrapper script {WRAPPER_SCRIPT} does not exist."
    assert os.access(WRAPPER_SCRIPT, os.X_OK), f"Wrapper script {WRAPPER_SCRIPT} is not executable."

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing."
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No JSON files found in clean corpus."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([WRAPPER_SCRIPT, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (or script failed): {failed_files}"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing."
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No JSON files found in evil corpus."

    bypassed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([WRAPPER_SCRIPT, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append((filename, result.returncode))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil payloads bypassed the WAF (expected exit code 1): {[f[0] for f in bypassed_files]}"