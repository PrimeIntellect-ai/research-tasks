# test_final_state.py
import os
import subprocess
import re

def test_api_secret():
    secret_path = "/home/user/api_secret.txt"
    assert os.path.isfile(secret_path), f"{secret_path} is missing."
    with open(secret_path, "r") as f:
        content = f.read().strip()
    assert content == "sre-core-auth-992x-alpha", f"Incorrect secret in {secret_path}. Found: {content}"

def test_ping_count():
    count_path = "/home/user/ping_count.txt"
    assert os.path.isfile(count_path), f"{count_path} is missing."
    with open(count_path, "r") as f:
        content = f.read().strip()
    assert content == "15", f"Incorrect ping count in {count_path}. Expected 15, found: {content}"

def test_tracker_c_patched():
    tracker_path = "/home/user/uptime_tracker/tracker.c"
    assert os.path.isfile(tracker_path), f"{tracker_path} is missing."
    with open(tracker_path, "r") as f:
        content = f.read()

    # The bug was `i <= WINDOW_SIZE`, it should be `i < WINDOW_SIZE`
    assert "i < WINDOW_SIZE" in content or "i<WINDOW_SIZE" in content or "i < 5" in content or "i<5" in content, \
        "The off-by-one bug in tracker.c does not appear to be fixed (expected loop condition to use < instead of <=)."
    assert "i <= WINDOW_SIZE" not in content and "i<=WINDOW_SIZE" not in content, \
        "The off-by-one bug (<=) is still present in tracker.c."

def test_trace_log():
    log_path = "/home/user/trace.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. Did you run the compiled tracker?"
    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Step 0 sum: 99.90",
        "Step 1 sum: 199.90",
        "Step 2 sum: 295.40",
        "Step 3 sum: 394.40",
        "Step 4 sum: 492.60"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(lines)}."
    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {log_path} is incorrect. Expected '{expected}', found '{actual}'."

def test_compilation_and_execution():
    tracker_dir = "/home/user/uptime_tracker"
    tracker_src = os.path.join(tracker_dir, "tracker.c")
    tracker_bin = os.path.join(tracker_dir, "tracker")

    # Re-compile to ensure it compiles without error
    compile_proc = subprocess.run(
        ["gcc", "-o", tracker_bin, tracker_src],
        cwd=tracker_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert compile_proc.returncode == 0, f"Compilation failed:\n{compile_proc.stderr.decode()}"

    # Run to ensure no segfaults
    run_proc = subprocess.run(
        [tracker_bin],
        cwd=tracker_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert run_proc.returncode == 0, f"Execution failed (possible segfault or error):\n{run_proc.stderr.decode()}"