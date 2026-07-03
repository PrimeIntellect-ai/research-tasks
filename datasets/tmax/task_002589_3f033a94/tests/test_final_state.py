# test_final_state.py
import os
import subprocess
import pytest

EVIL_DIR = '/app/corpus/evil/'
CLEAN_DIR = '/app/corpus/clean/'
BINARY_PATH = '/home/user/waf_filter'

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Binary {BINARY_PATH} does not exist. Did you compile it?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary {BINARY_PATH} is not executable."

def test_waf_filter_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, "Evil corpus is empty."

    bypassed = []
    for f in evil_files:
        filepath = os.path.join(EVIL_DIR, f)
        try:
            result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "EVIL":
                bypassed.append(f)
        except subprocess.TimeoutExpired:
            bypassed.append(f"{f} (timeout)")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed}")

def test_waf_filter_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "Clean corpus is empty."

    modified = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_DIR, f)
        try:
            result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "CLEAN":
                modified.append(f)
        except subprocess.TimeoutExpired:
            modified.append(f"{f} (timeout)")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified: {modified}")