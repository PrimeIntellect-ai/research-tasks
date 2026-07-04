# test_final_state.py
import os
import subprocess
import urllib.request
import json
import time

def test_environment_variables():
    profile_path = "/home/user/.bash_profile"
    assert os.path.isfile(profile_path), f"{profile_path} does not exist."
    with open(profile_path, "r") as f:
        content = f.read()
    assert "BACKEND1_PORT=9001" in content or "BACKEND1_PORT=\"9001\"" in content or "BACKEND1_PORT='9001'" in content, "BACKEND1_PORT=9001 not found in .bash_profile"
    assert "BACKEND2_PORT=9002" in content or "BACKEND2_PORT=\"9002\"" in content or "BACKEND2_PORT='9002'" in content, "BACKEND2_PORT=9002 not found in .bash_profile"

def test_proxy_and_load_balancing():
    # Make 10 requests to the proxy
    proxy_url = "http://127.0.0.1:8080/"
    responses = []
    for _ in range(10):
        try:
            req = urllib.request.Request(proxy_url)
            with urllib.request.urlopen(req, timeout=2) as response:
                responses.append(response.read().decode('utf-8').strip())
        except Exception as e:
            assert False, f"Request to proxy failed: {e}"

    # We expect the responses to contain some identifier of backend1 and backend2.
    # Since they are dummy servers started by start_services.sh, they likely return their port or directory.
    # We just count the distinct responses. Since it's round-robin, there should be exactly 5 of one and 5 of the other.
    counts = {}
    for r in responses:
        counts[r] = counts.get(r, 0) + 1

    assert len(counts) == 2, f"Expected responses from exactly 2 backends, got {len(counts)} distinct responses: {counts}"
    for k, v in counts.items():
        assert v == 5, f"Expected 5 requests per backend, got {v} for backend {k}"

def test_adversarial_filter():
    filter_bin = "/home/user/filter"
    assert os.path.isfile(filter_bin), f"Filter binary {filter_bin} not found."
    assert os.access(filter_bin, os.X_OK), f"Filter binary {filter_bin} is not executable."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run([filter_bin, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run([filter_bin, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    assert len(clean_failed) == 0, f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {clean_failed}"
    assert len(evil_failed) == 0, f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted): {evil_failed}"

def test_storage_monitoring():
    monitor_script = "/home/user/monitor.sh"
    assert os.path.isfile(monitor_script), f"Monitor script {monitor_script} not found."
    assert os.access(monitor_script, os.X_OK), f"Monitor script {monitor_script} is not executable."

    logs_dir = "/home/user/logs"
    os.makedirs(logs_dir, exist_ok=True)

    # Clean the directory first
    for f in os.listdir(logs_dir):
        os.remove(os.path.join(logs_dir, f))

    # Test OK state (size < 50000)
    res = subprocess.run([monitor_script], capture_output=True, text=True)
    assert res.stdout.strip() == "OK", f"Expected 'OK' when size is small, got '{res.stdout.strip()}'"

    # Test WARNING state (size > 50000)
    big_file = os.path.join(logs_dir, "big_file.log")
    with open(big_file, "wb") as f:
        f.write(b"0" * 60000)

    try:
        res = subprocess.run([monitor_script], capture_output=True, text=True)
        assert res.stdout.strip() == "WARNING: QUOTA EXCEEDED", f"Expected 'WARNING: QUOTA EXCEEDED', got '{res.stdout.strip()}'"
    finally:
        os.remove(big_file)