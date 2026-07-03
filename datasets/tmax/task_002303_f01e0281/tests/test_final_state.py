# test_final_state.py

import os
import time
import subprocess
import urllib.request
import pytest

def test_port_forwarding():
    """Check if the port forwarding is correctly configured and services can communicate."""
    try:
        req = urllib.request.urlopen('http://127.0.0.1:9003', timeout=2)
        res = req.read().decode('utf-8')
        assert res == 'Frontend->Backend->DB_OK', f"Unexpected response from frontend: {res}"
    except Exception as e:
        pytest.fail(f"Failed to connect to frontend or invalid response (port forwarding might be broken): {e}")

def test_tmpfs_mount():
    """Check if /app/logs is a tmpfs mount with a maximum size of 50M."""
    try:
        out = subprocess.check_output('mount', shell=True).decode('utf-8')
        mount_lines = [l for l in out.splitlines() if '/app/logs' in l and 'tmpfs' in l]
        assert len(mount_lines) > 0, "tmpfs is not mounted at /app/logs"

        mount_line = mount_lines[0]
        assert 'size=50M' in mount_line or 'size=51200k' in mount_line or 'size=52428800' in mount_line, \
            f"Size 50M constraint not found in mount options: {mount_line}"
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute mount command")

def test_git_automation():
    """Check if the bare git repository and post-receive hook are configured correctly."""
    hook_path = '/home/user/monitor.git/hooks/post-receive'
    assert os.path.isfile(hook_path), f"Git hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Git hook at {hook_path} is not executable"

    exe_path = '/app/bin/alert_parser'
    assert os.path.isfile(exe_path), f"Compiled executable not found at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_final_output_exists():
    """Check if the final alerts output file exists."""
    assert os.path.isfile('/app/logs/alerts.txt'), "Final output /app/logs/alerts.txt is missing"

def test_c_parser_performance_and_accuracy():
    """Evaluate the C parser for precision, recall, and execution time against a massive log file."""
    exe_path = '/app/bin/alert_parser'
    assert os.path.isfile(exe_path), f"Executable missing at {exe_path}"

    test_log = '/tmp/massive_test.log'
    expected_txids = set()

    # Generate a massive log file (1,000,000 lines)
    with open(test_log, 'w') as f:
        for i in range(1_000_000):
            if i % 20 == 0:
                txid = f"SLOW{i}"
                time_ms = 501 + (i % 100)
                expected_txids.add(txid)
            else:
                txid = f"FAST{i}"
                time_ms = 10 + (i % 100)
            f.write(f"[2023-10-12T10:00:00] txid={txid} status=200 time={time_ms}ms\n")

    # Measure execution time
    start_time = time.time()
    try:
        out = subprocess.check_output([exe_path, test_log]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executable failed to run: {e}")
    exec_time = time.time() - start_time

    actual_txids = set(out.strip().split())

    # Check accuracy
    missing = expected_txids - actual_txids
    extra = actual_txids - expected_txids
    assert not missing and not extra, "Precision and recall are not exactly 1.0 (missing or extra txids found)"

    # Check performance threshold
    assert exec_time <= 0.2, f"Execution time {exec_time:.3f}s exceeds the threshold of 0.2s"