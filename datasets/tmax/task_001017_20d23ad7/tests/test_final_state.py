# test_final_state.py

import os
import subprocess
import time
import json
import pytest

def test_fast_backup_exists_and_executable():
    path = "/home/user/fast_backup"
    assert os.path.exists(path), f"File {path} does not exist. Did you compile your C program?"
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_fast_backup_correctness_and_speedup():
    legacy_bin = "/app/legacy_backup_bin"
    fast_bin = "/home/user/fast_backup"

    root_node = "42"
    max_depth = "3"
    page_size = "50"
    page_num = "0"

    # Run Legacy
    start_leg = time.time()
    try:
        leg_out = subprocess.check_output([legacy_bin, root_node, max_depth, page_size, page_num], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Legacy binary failed: {e.output.decode('utf-8', errors='ignore')}")
    leg_time = time.time() - start_leg

    # Run Fast
    start_fast = time.time()
    try:
        fast_out = subprocess.check_output([fast_bin, root_node, max_depth, page_size, page_num], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Your fast_backup binary failed: {e.output.decode('utf-8', errors='ignore')}")
    fast_time = time.time() - start_fast

    speedup = leg_time / max(fast_time, 0.001)

    try:
        leg_json = json.loads(leg_out.decode('utf-8'))
    except json.JSONDecodeError:
        pytest.fail("Legacy binary did not output valid JSON.")

    try:
        fast_json = json.loads(fast_out.decode('utf-8'))
    except json.JSONDecodeError:
        pytest.fail("Your fast_backup binary did not output valid JSON.")

    assert leg_json == fast_json, f"Output mismatch. Expected: {leg_json}, Got: {fast_json}"
    assert speedup >= 50.0, f"Speedup too low. Required: >= 50.0x, Achieved: {speedup:.2f}x (Legacy time: {leg_time:.4f}s, Fast time: {fast_time:.4f}s)"