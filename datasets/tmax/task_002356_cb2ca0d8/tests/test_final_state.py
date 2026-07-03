# test_final_state.py

import os
import subprocess
import time
import urllib.request
import pytest

def test_go_binaries_exist():
    amd64_path = "/home/user/app/go-auth/build/auth-amd64"
    arm64_path = "/home/user/app/go-auth/build/auth-arm64"

    assert os.path.isfile(amd64_path), f"Missing Go binary: {amd64_path}"
    assert os.path.isfile(arm64_path), f"Missing Go binary: {arm64_path}"

    # Check if they are executable
    assert os.access(amd64_path, os.X_OK), f"Binary is not executable: {amd64_path}"
    assert os.access(arm64_path, os.X_OK), f"Binary is not executable: {arm64_path}"

def test_detector_script_against_corpus():
    detector_path = "/home/user/detector.sh"
    assert os.path.isfile(detector_path), f"Missing detector script: {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector script is not executable: {detector_path}"

    clean_dir = "/home/user/corpus/clean"
    evil_dir = "/home/user/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run([detector_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run([detector_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    assert not error_messages, " | ".join(error_messages)

def test_services_integration():
    start_script = "/home/user/start_services.sh"
    assert os.path.isfile(start_script), f"Missing startup script: {start_script}"
    assert os.access(start_script, os.X_OK), f"Startup script is not executable: {start_script}"

    # Execute the startup script
    subprocess.run([start_script], shell=True, check=True)

    # Allow some time for services to start
    time.sleep(3)

    # Test Nginx routing to Flask
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/api/ping", method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8')
            assert "pong" in body, "Flask service did not return expected response through Nginx"
    except Exception as e:
        pytest.fail(f"Failed to reach Flask service via Nginx: {e}")

    # Test Nginx routing to Go Auth
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/auth/login", method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8')
            assert "authenticated" in body, "Go auth service did not return expected response through Nginx"
    except Exception as e:
        pytest.fail(f"Failed to reach Go auth service via Nginx: {e}")

    # Verify Nginx config modifications
    nginx_conf_path = "/home/user/app/nginx/nginx.conf"
    with open(nginx_conf_path, 'r') as f:
        conf_content = f.read()

    assert "proxy_pass" in conf_content, "Nginx config missing proxy_pass directives"
    assert "8081" in conf_content, "Nginx config missing proxy to Flask port 8081"
    assert "8082" in conf_content, "Nginx config missing proxy to Go auth port 8082"