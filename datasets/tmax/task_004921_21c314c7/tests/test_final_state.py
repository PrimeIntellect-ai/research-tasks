# test_final_state.py

import os
import stat
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/filter.sh"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_filter_script_exists_and_executable():
    assert os.path.isfile(FILTER_SCRIPT), f"Filter script not found at {FILTER_SCRIPT}"
    st = os.stat(FILTER_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Filter script at {FILTER_SCRIPT} is not executable"

def test_filter_script_behavior():
    # Gather corpus files
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    bypassed_evil = []
    modified_clean = []

    # Test evil corpus (expected exit code 1)
    for evil_file in evil_files:
        result = subprocess.run([FILTER_SCRIPT, evil_file], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(evil_file))

    # Test clean corpus (expected exit code 0)
    for clean_file in clean_files:
        result = subprocess.run([FILTER_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(clean_file))

    # Construct failure message
    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    assert not errors, " | ".join(errors)