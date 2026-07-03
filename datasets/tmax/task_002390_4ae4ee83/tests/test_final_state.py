# test_final_state.py

import os
import subprocess
import pytest

WAF_SCRIPT = "/home/user/waf.sh"
EVIL_CORPUS_DIR = "/verify/corpus/evil"
CLEAN_CORPUS_DIR = "/verify/corpus/clean"

def test_waf_script_exists_and_executable():
    assert os.path.exists(WAF_SCRIPT), f"WAF script not found at {WAF_SCRIPT}"
    assert os.path.isfile(WAF_SCRIPT), f"{WAF_SCRIPT} is not a file"
    assert os.access(WAF_SCRIPT, os.X_OK), f"WAF script at {WAF_SCRIPT} is not executable"

def test_waf_evil_corpus():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory {EVIL_CORPUS_DIR} not found")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([WAF_SCRIPT, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil requests bypassed the WAF: {', '.join(bypassed_files)}")

def test_waf_clean_corpus():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory {CLEAN_CORPUS_DIR} not found")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    blocked_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([WAF_SCRIPT, filepath], capture_output=True)
        if result.returncode != 0:
            blocked_files.append(filename)

    if blocked_files:
        pytest.fail(f"{len(blocked_files)} of {len(clean_files)} clean requests were incorrectly blocked by the WAF: {', '.join(blocked_files)}")