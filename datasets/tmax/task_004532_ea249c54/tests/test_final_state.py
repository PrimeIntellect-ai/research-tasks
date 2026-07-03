# test_final_state.py
import os
import socket
import subprocess
import time
import glob
import requests
import pytest

def get_stats():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(('127.0.0.1', 8084))
        s.sendall(b"STATS\n")
        data = s.recv(1024).decode('utf-8')
        s.close()
        if data.startswith("PROCESSED="):
            return int(data.strip().split("=")[1])
    except Exception as e:
        pytest.fail(f"Failed to connect to TCP admin server on 8084 or parse stats: {e}")
    return 0

def test_proxy_routing_and_stats():
    # Get initial stats
    initial_stats = get_stats()

    # 1. POST with NO headers
    try:
        resp1 = requests.post("http://127.0.0.1:8080/process", data="test", timeout=2)
        assert resp1.status_code == 200, f"Expected HTTP 200, got {resp1.status_code}"
        assert "EXPENSIVE_TIER_RESULT" in resp1.text, f"Expected EXPENSIVE_TIER_RESULT, got {resp1.text}"
    except requests.RequestException as e:
        pytest.fail(f"Request 1 failed: {e}")

    # 2. POST with X-Tier: Spot
    try:
        resp2 = requests.post("http://127.0.0.1:8080/process", headers={"X-Tier": "Spot"}, data="test", timeout=2)
        assert resp2.status_code == 200, f"Expected HTTP 200, got {resp2.status_code}"
        assert "CHEAP_TIER_RESULT" in resp2.text, f"Expected CHEAP_TIER_RESULT, got {resp2.text}"
    except requests.RequestException as e:
        pytest.fail(f"Request 2 failed: {e}")

    # 3. POST with X-Tier: OnDemand
    try:
        resp3 = requests.post("http://127.0.0.1:8080/process", headers={"X-Tier": "OnDemand"}, data="test", timeout=2)
        assert resp3.status_code == 200, f"Expected HTTP 200, got {resp3.status_code}"
        assert "EXPENSIVE_TIER_RESULT" in resp3.text, f"Expected EXPENSIVE_TIER_RESULT, got {resp3.text}"
    except requests.RequestException as e:
        pytest.fail(f"Request 3 failed: {e}")

    # Get final stats
    final_stats = get_stats()
    assert final_stats == initial_stats + 3, f"Expected stats to increment by 3, but went from {initial_stats} to {final_stats}"

def test_deploy_script_exists_and_executable():
    assert os.path.isfile("/home/user/deploy.sh"), "/home/user/deploy.sh does not exist"
    assert os.access("/home/user/deploy.sh", os.X_OK), "/home/user/deploy.sh is not executable"

def test_backup_script():
    backup_script = "/home/user/backup.sh"
    assert os.path.isfile(backup_script), f"{backup_script} does not exist"
    assert os.access(backup_script, os.X_OK), f"{backup_script} is not executable"

    # Count existing backups
    backup_dir = "/home/user/backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    initial_backups = len(glob.glob(os.path.join(backup_dir, "proxy_*.log.gz")))

    # Run backup script
    result = subprocess.run([backup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Backup script failed with exit code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    final_backups = len(glob.glob(os.path.join(backup_dir, "proxy_*.log.gz")))
    assert final_backups > initial_backups, "Backup script did not create a new .log.gz file in /home/user/backups/"