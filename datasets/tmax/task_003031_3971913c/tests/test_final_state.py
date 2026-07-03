# test_final_state.py
import os
import time
import requests
import subprocess

def test_done_file():
    done_path = '/app/done.txt'
    assert os.path.isfile(done_path), f"{done_path} is missing."
    with open(done_path, 'r') as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected 'SUCCESS' in {done_path}, got '{content}'."

def test_squashfuse_mount():
    # Check if squashfuse is running and mounting /app/data
    try:
        output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
        assert 'squashfuse' in output and '/app/data' in output, "squashfuse is not running or not mounting /app/data."
    except subprocess.CalledProcessError:
        assert False, "Failed to check running processes for squashfuse."

def test_fstab_entry():
    fstab_path = '/app/restore-env/fstab'
    assert os.path.isfile(fstab_path), f"{fstab_path} is missing."
    with open(fstab_path, 'r') as f:
        content = f.read()
    expected_line = "/app/backup.sqsh /app/data squashfs defaults 0 0"
    assert expected_line in content, f"Expected fstab entry '{expected_line}' not found in {fstab_path}."

def test_nginx_and_go_performance():
    url = "http://localhost:8080/stats"
    start = time.time()
    try:
        r = requests.get(url, timeout=2.0)
        elapsed = time.time() - start
    except requests.RequestException as e:
        assert False, f"Request to {url} failed: {e}"

    assert r.status_code == 200, f"Expected HTTP 200, got {r.status_code}. Response: {r.text[:100]}"
    assert elapsed <= 0.250, f"Latency threshold failed: {elapsed:.3f}s > 0.250s. The Go application needs further optimization."

def test_ssh_tunnel():
    url = "http://localhost:9090/debug/pprof/"
    try:
        r = requests.get(url, timeout=2.0)
    except requests.RequestException as e:
        assert False, f"SSH tunnel check failed. Could not reach {url}: {e}"

    assert r.status_code == 200, f"Expected HTTP 200 from internal pprof endpoint, got {r.status_code}."