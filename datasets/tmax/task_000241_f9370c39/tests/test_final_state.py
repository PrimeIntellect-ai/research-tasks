# test_final_state.py

import os
import sys
import json
import socket
import urllib.request
import urllib.error
import pytest
import importlib.util

def test_sanitizer_adversarial_corpus():
    sanitizer_path = '/home/user/sanitizer.py'
    assert os.path.isfile(sanitizer_path), f"Sanitizer module not found at {sanitizer_path}"

    spec = importlib.util.spec_from_file_location("sanitizer", sanitizer_path)
    sanitizer = importlib.util.module_from_spec(spec)
    sys.modules["sanitizer"] = sanitizer
    try:
        spec.loader.exec_module(sanitizer)
    except Exception as e:
        pytest.fail(f"Failed to load sanitizer.py: {e}")

    assert hasattr(sanitizer, 'is_safe'), "sanitizer.py does not define is_safe function"
    is_safe = sanitizer.is_safe

    evil_dir = '/home/user/corpus/evil/'
    clean_dir = '/home/user/corpus/clean/'

    evil_files = sorted([f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])
    clean_files = sorted([f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])

    assert len(evil_files) > 0, "Evil corpus is empty"
    assert len(clean_files) > 0, "Clean corpus is empty"

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        with open(os.path.join(evil_dir, f), 'rb') as file:
            content = file.read()
            try:
                if is_safe(content) is not False:
                    evil_bypassed.append(f)
            except Exception:
                evil_bypassed.append(f)

    for f in clean_files:
        with open(os.path.join(clean_dir, f), 'rb') as file:
            content = file.read()
            try:
                if is_safe(content) is not True:
                    clean_modified.append(f)
            except Exception:
                clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {evil_bypassed}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {clean_modified}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_router_config_updated():
    config_path = '/home/user/router_config.json'
    assert os.path.isfile(config_path), f"Router config not found at {config_path}"
    with open(config_path, 'r') as f:
        config = json.load(f)
    assert config.get("downstream_url") == "http://127.0.0.1:8082", "Router config downstream_url not updated to point to the proxy (http://127.0.0.1:8082)"

def test_proxy_running():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        try:
            s.connect(('127.0.0.1', 8082))
        except (ConnectionRefusedError, socket.timeout, OSError):
            pytest.fail("Proxy is not listening on 127.0.0.1:8082")

def test_end_to_end_flow():
    # Test safe payload
    safe_payload = b'{"timestamp": "2023-10-01T12:00:00Z", "message": "Normal log message"}'
    req = urllib.request.Request('http://127.0.0.1:8080', data=safe_payload, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status in (200, 201, 202, 204), f"Expected success status for safe payload, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to send safe payload to router: {e}")

    # Test evil payload
    evil_payload = b'{"timestamp": "2023-10-01T12:00:01Z", "message": "Evil log message \\ud800"}'
    req = urllib.request.Request('http://127.0.0.1:8080', data=evil_payload, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            pytest.fail(f"Expected 400 series error for evil payload, but request succeeded with status {response.status}")
    except urllib.error.HTTPError as e:
        assert 400 <= e.code < 500, f"Expected 400 series error for evil payload, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to send evil payload to router: {e}")