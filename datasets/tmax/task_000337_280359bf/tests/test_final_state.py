# test_final_state.py

import os
import time
import subprocess
import urllib.request
import urllib.error
import json
import pytest

def test_setup_complete_log():
    log_path = "/home/user/setup_complete.log"
    assert os.path.isfile(log_path), f"Missing log file at {log_path}"
    with open(log_path, "r") as f:
        content = f.read()
    assert "READY" in content, f"Log file {log_path} does not contain 'READY'"

def test_mount_and_fstab():
    # Check mount
    with open("/proc/mounts", "r") as f:
        mounts = f.read()
    assert "/home/user/user_data_mnt" in mounts, "/app/user_data.img is not mounted at /home/user/user_data_mnt"

    # Check fstab
    fstab_path = "/home/user/local_fstab"
    assert os.path.isfile(fstab_path), f"Missing local fstab at {fstab_path}"
    with open(fstab_path, "r") as f:
        fstab_content = f.read()
    assert "/app/user_data.img" in fstab_content and "/home/user/user_data_mnt" in fstab_content, "local_fstab does not contain the correct mount entry"

def test_services_and_corpus():
    script_path = "/home/user/start_services.sh"
    assert os.path.isfile(script_path), f"Missing startup script at {script_path}"
    assert os.access(script_path, os.X_OK), f"Startup script {script_path} is not executable"

    # Run the startup script
    subprocess.run(["bash", script_path], check=True)

    # Wait for health endpoint
    health_url = "http://127.0.0.1:8080/health"
    max_retries = 10
    health_ok = False
    for _ in range(max_retries):
        try:
            req = urllib.request.Request(health_url)
            with urllib.request.urlopen(req, timeout=1) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    if data.get("status") == "ok":
                        health_ok = True
                        break
        except Exception:
            pass
        time.sleep(1)

    assert health_ok, "Proxy health endpoint did not return 200 OK with {'status': 'ok'} within 10 seconds"

    # Test evil corpus
    evil_dir = "/app/corpus/evil"
    evil_files = os.listdir(evil_dir)
    evil_bypassed = []
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        with open(path, "rb") as file:
            payload = file.read()
        try:
            req = urllib.request.Request("http://127.0.0.1:8080/process", data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status != 403:
                    evil_bypassed.append(f)
        except urllib.error.HTTPError as e:
            if e.code != 403:
                evil_bypassed.append(f)
        except Exception:
            evil_bypassed.append(f)

    # Test clean corpus
    clean_dir = "/app/corpus/clean"
    clean_files = os.listdir(clean_dir)
    clean_modified = []
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        with open(path, "rb") as file:
            payload = file.read()
        try:
            req = urllib.request.Request("http://127.0.0.1:8080/process", data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status != 200:
                    clean_modified.append(f)
        except Exception:
            clean_modified.append(f)

    assert not evil_bypassed, f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}"
    assert not clean_modified, f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}"