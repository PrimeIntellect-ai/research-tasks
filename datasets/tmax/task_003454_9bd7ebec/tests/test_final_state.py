# test_final_state.py

import os
import pytest

def test_setup_script_fixed():
    path = "/home/user/app/setup.sh"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "LOK_DIR" not in content, f"{path} still contains the misspelled variable 'LOK_DIR'."
    assert "LOCK_DIR" in content, f"{path} should contain the correct variable 'LOCK_DIR'."

def test_directories_and_locks_created():
    log_dir = "/home/user/app/logs"
    lock_dir = "/home/user/app/locks"
    assert os.path.isdir(log_dir), f"Directory {log_dir} does not exist. Did setup.sh run?"
    assert os.path.isdir(lock_dir), f"Directory {lock_dir} does not exist. Did setup.sh run?"

    lock_a = os.path.join(lock_dir, "a.lock")
    lock_b = os.path.join(lock_dir, "b.lock")
    assert os.path.isfile(lock_a), f"Lock file {lock_a} is missing."
    assert os.path.isfile(lock_b), f"Lock file {lock_b} is missing."

def test_result_log_content():
    result_log = "/home/user/app/logs/result.log"
    assert os.path.isfile(result_log), f"Result log {result_log} is missing. Did log_aggregator.sh complete?"

    with open(result_log, "r") as f:
        content = f.read()

    assert "Worker 1 done" in content, f"'Worker 1 done' not found in {result_log}."
    assert "Worker 2 done" in content, f"'Worker 2 done' not found in {result_log}."
    assert "All done" in content, f"'All done' not found in {result_log}."