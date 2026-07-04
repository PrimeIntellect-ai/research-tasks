# test_final_state.py
import os
import subprocess
import urllib.request
import urllib.error
import socket
import pytest
import glob

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def test_classifier_executable():
    classifier_path = "/home/user/classifier"
    assert os.path.isfile(classifier_path), f"Classifier not found at {classifier_path}"
    assert os.access(classifier_path, os.X_OK), f"Classifier at {classifier_path} is not executable"

def test_classifier_corpus():
    classifier_path = "/home/user/classifier"
    clean_dir = "/home/user/workspace/corpus/clean"
    evil_dir = "/home/user/workspace/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    clean_modified = []
    for f in clean_files:
        res = subprocess.run([classifier_path, f], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(f))

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run([classifier_path, f], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)

def test_services_running():
    assert check_port(6379), "Redis is not listening on port 6379"
    assert check_port(5000), "Python API is not listening on port 5000"
    assert check_port(8080), "Nginx is not listening on port 8080"

def test_nginx_proxy():
    # Test that Nginx is proxying to the API
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=2) as response:
            pass # Just checking if it responds without Nginx 502 Bad Gateway
    except urllib.error.HTTPError as e:
        # 404 or 405 is fine, it means the API responded
        assert e.code in [404, 405, 422], f"Expected API response, got HTTP {e.code}"
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx proxy: {e}")