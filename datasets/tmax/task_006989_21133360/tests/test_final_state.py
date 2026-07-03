# test_final_state.py

import os
import re
import pytest

def test_resolution_output():
    path = "/home/user/resolution.txt"
    assert os.path.exists(path), f"File {path} is missing. Did you run the script and redirect output?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert "Final processed count: 10000" in content, "The resolution.txt does not contain the expected final count."

def test_start_sh_fixed():
    path = "/home/user/event-ingester/start.sh"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check that BATCH_SIZE is no longer "0"
    match = re.search(r'export BATCH_SIZE=["\']?(\d+)["\']?', content)
    assert match is not None, "Could not find BATCH_SIZE export in start.sh."
    assert match.group(1) != "0", "BATCH_SIZE is still set to 0 in start.sh, which causes a panic."

def test_main_rs_fixed_bugs():
    path = "/home/user/event-ingester/src/main.rs"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check statistical anomaly is removed
    assert "i % 100" not in content, "The statistical anomaly (modulo 100 drop) is still present in main.rs."

    # Check concurrency bug is fixed
    # The original code had:
    # let current = metrics_clone.lock().unwrap().processed;
    # metrics_clone.lock().unwrap().processed = current + 1;
    # We should ensure that we don't have this split read/write pattern.
    split_lock_pattern = re.search(r'let\s+\w+\s*=\s*.*?\.lock\(\).*?;\s*.*?\.lock\(\).*?=', content, re.DOTALL)
    assert not split_lock_pattern, "The logical race condition (split lock read-modify-write) is still present in main.rs."

    # Ensure there is a lock modification (e.g. += 1 or similar)
    assert ".lock()" in content, "No lock acquisition found in main.rs."