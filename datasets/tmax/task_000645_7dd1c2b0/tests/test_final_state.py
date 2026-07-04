# test_final_state.py
import os
import re

def test_minimal_crash_log():
    crash_log_path = "/home/user/minimal_crash.log"
    assert os.path.isfile(crash_log_path), f"{crash_log_path} does not exist."

    with open(crash_log_path, "r") as f:
        content = f.read().strip()

    expected_line = "2023-10-15 03:14:15 [ERROR] FATAL_PAYLOAD_0x8A payload=null"
    assert content == expected_line, f"Content of {crash_log_path} is incorrect. Expected exactly the crashing line."

def test_worker_c_fixes():
    worker_c_path = "/home/user/sensor_service/worker.c"
    assert os.path.isfile(worker_c_path), f"{worker_c_path} does not exist."

    with open(worker_c_path, "r") as f:
        content = f.read()

    # Check for race condition fix (mutex or atomic)
    has_mutex = "pthread_mutex_t" in content and ("pthread_mutex_lock" in content or "pthread_mutex_trylock" in content)
    has_atomic = "_Atomic" in content or "__atomic_" in content or "__sync_" in content

    assert has_mutex or has_atomic, "worker.c does not seem to include a mutex or atomic operation to fix the race condition."

    # Check for struct tm initialization
    has_memset = "memset" in content and "tm" in content
    has_zero_init = "= {0}" in content or "= { 0 }" in content

    assert has_memset or has_zero_init, "worker.c does not properly initialize `struct tm` (e.g., using memset or = {0})."

def test_success_out():
    success_out_path = "/home/user/success.out"
    assert os.path.isfile(success_out_path), f"{success_out_path} does not exist."

    with open(success_out_path, "r") as f:
        content = f.read()

    assert "Processing complete. Corrupted packets: " in content, f"{success_out_path} does not contain the expected success message."

def test_binary_compiled():
    binary_path = "/home/user/sensor_service/sensor_sync"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."