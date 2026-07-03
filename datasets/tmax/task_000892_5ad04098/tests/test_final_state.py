# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

EVIL_DIR = "/home/user/data/evil"
CLEAN_DIR = "/home/user/data/clean"
URL = "http://localhost:8080/sanitize"

def send_request(text):
    data = json.dumps({"text": text}).encode('utf-8')
    req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return None

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory {EVIL_DIR} not found."
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory {CLEAN_DIR} not found."

    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        with open(os.path.join(EVIL_DIR, f), 'r', encoding='utf-8') as file:
            content = file.read()
        res = send_request(content)
        if res is None or res.get("safe") is not False:
            evil_bypassed.append(f)

    for f in clean_files:
        with open(os.path.join(CLEAN_DIR, f), 'r', encoding='utf-8') as file:
            content = file.read()
        res = send_request(content)
        if res is None or res.get("safe") is not True:
            clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected or failed): {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_pyproject_toml_fixed():
    path = "/home/user/app/sanitizer-app/pyproject.toml"
    assert os.path.isfile(path), f"Expected {path} to exist."
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    assert "flask" in content, "Flask dependency missing from pyproject.toml"
    assert "redis" in content, "Redis dependency missing from pyproject.toml"

def test_detector_py_exists():
    path = "/home/user/app/sanitizer-app/sanitizer/detector.py"
    assert os.path.isfile(path), f"Expected {path} to exist."

def test_app_py_exists():
    path = "/home/user/app/sanitizer-app/sanitizer/app.py"
    assert os.path.isfile(path), f"Expected {path} to exist."

def test_test_app_py_exists():
    path = "/home/user/app/sanitizer-app/tests/test_app.py"
    assert os.path.isfile(path), f"Expected {path} to exist."

def test_nginx_conf_fixed():
    path = "/home/user/app/nginx/nginx.conf"
    assert os.path.isfile(path), f"Expected {path} to exist."
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:5000;" in content or "proxy_pass http://localhost:5000;" in content, "Nginx config does not contain the correct proxy_pass directive."