# test_final_state.py
import os
import json
import subprocess
import pytest
import time
import socket
import threading

APP_DIR = "/home/user/app"

def test_report_json():
    report_path = os.path.join(APP_DIR, "report.json")
    assert os.path.isfile(report_path), "report.json is missing"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not valid JSON")

    assert "pcap_final_dst_port" in report, "Missing pcap_final_dst_port in report.json"
    assert report["pcap_final_dst_port"] == 8888, f"Expected pcap_final_dst_port to be 8888, got {report['pcap_final_dst_port']}"

    assert "deadlock_cause" in report, "Missing deadlock_cause in report.json"
    assert isinstance(report["deadlock_cause"], str) and len(report["deadlock_cause"]) > 0, "deadlock_cause must be a non-empty string"

def test_runner_sh_fixed():
    runner_path = os.path.join(APP_DIR, "runner.sh")
    assert os.path.isfile(runner_path), "runner.sh is missing"

    with open(runner_path, "r") as f:
        content = f.read()

    assert "$(ls" not in content, "runner.sh still uses the buggy '$(ls ...)' pattern which breaks on spaces."

def test_server_py_fixed():
    server_path = os.path.join(APP_DIR, "server.py")
    assert os.path.isfile(server_path), "server.py is missing"

    with open(server_path, "r") as f:
        content = f.read()

    # The fix could be using `with stats_lock:` or adding `stats_lock.release()` in the ERROR branch.
    # We will check if the deadlock is actually fixed by running mre.py, but we can also do a simple check.
    # If they still have stats_lock.acquire(), they must have multiple release() calls or a finally block.
    if "stats_lock.acquire()" in content:
        assert content.count("stats_lock.release()") >= 2 or "finally:" in content, "server.py still seems to leak the lock on the error branch."

def test_mre_py_runs_successfully():
    mre_path = os.path.join(APP_DIR, "mre.py")
    assert os.path.isfile(mre_path), "mre.py is missing"

    # Run mre.py with a timeout to verify it doesn't hang
    try:
        result = subprocess.run(
            ["python3", mre_path],
            cwd=APP_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True
        )
        assert result.returncode == 0, f"mre.py failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("mre.py timed out after 5 seconds, indicating the deadlock is still present or the script is hanging.")