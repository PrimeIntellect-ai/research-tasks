# test_final_state.py

import os
import gzip
import pytest

WORKSPACE_DIR = "/home/user/migration_test"

def test_memory_leak_fixed():
    proxy_path = os.path.join(WORKSPACE_DIR, "proxy.go")
    assert os.path.isfile(proxy_path), f"{proxy_path} does not exist."

    with open(proxy_path, "r") as f:
        content = f.read()

    assert "GlobalLeakTracker = append" not in content, "The memory leak in proxy.go was not fixed (GlobalLeakTracker = append still exists)."

def test_memory_profile_generated():
    prof_path = os.path.join(WORKSPACE_DIR, "mem.prof")
    assert os.path.isfile(prof_path), f"Memory profile {prof_path} was not generated."

    # Check if it's a valid gzip file (pprof profiles are gzipped protobufs)
    try:
        with gzip.open(prof_path, "rb") as f:
            f.read(1)
    except Exception as e:
        pytest.fail(f"{prof_path} is not a valid gzip-compressed file (expected pprof format): {e}")

def test_diff_log_generated_and_correct():
    log_path = os.path.join(WORKSPACE_DIR, "diff_results.log")
    assert os.path.isfile(log_path), f"Diff log {log_path} was not generated."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Alice" in content and "Alice_New" in content, "The diff log does not contain the expected differences for firstName ('Alice' vs 'Alice_New')."

    # It should be a unified diff, so it should have typical diff markers
    assert "-" in content and "+" in content, "The diff log does not appear to contain a unified diff."