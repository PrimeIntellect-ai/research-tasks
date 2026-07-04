# test_final_state.py

import os
import sys
import json
import socket
import urllib.request
import urllib.error
import importlib.util
import pytest

def test_setup_complete_log():
    log_path = "/home/user/app/setup_complete.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read()
    assert "SYSTEM_READY" in content, f"Log file {log_path} does not contain 'SYSTEM_READY'."

def test_validator_logic():
    validator_path = "/home/user/app/gateway/validator.py"
    assert os.path.isfile(validator_path), f"Validator module {validator_path} is missing."

    spec = importlib.util.spec_from_file_location("validator", validator_path)
    validator = importlib.util.module_from_spec(spec)
    sys.modules["validator"] = validator
    spec.loader.exec_module(validator)

    assert hasattr(validator, "validate_build_request"), "Validator module missing 'validate_build_request' function."

    clean_dir = "/home/user/app/corpora/clean/"
    evil_dir = "/home/user/app/corpora/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for cf in clean_files:
        with open(cf, "r") as f:
            payload = f.read()
        try:
            result = validator.validate_build_request(payload)
            if not result:
                clean_failed.append(os.path.basename(cf))
        except Exception:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        with open(ef, "r") as f:
            payload = f.read()
        try:
            result = validator.validate_build_request(payload)
            if result:
                evil_failed.append(os.path.basename(ef))
        except Exception:
            # Exception is considered safe/false
            pass

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    assert not error_msgs, "Validator errors:\n" + "\n".join(error_msgs)

def test_services_running():
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    assert is_port_open(6379), "Redis service is not running on port 6379."
    assert is_port_open(5001), "Dispatcher service is not running on port 5001."
    assert is_port_open(5000), "Gateway service is not running on port 5000."

def test_gateway_routing_and_rate_limiting():
    url = "http://localhost:5000/webhook"

    clean_payload = json.dumps({
        "repository": "foo",
        "commit_hash": "abc1234",
        "build_target": "src/main"
    }).encode('utf-8')

    headers = {'Content-Type': 'application/json'}

    # Send up to 5 valid requests, they should succeed (return 200 OK)
    for i in range(5):
        req = urllib.request.Request(url, data=clean_payload, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                assert response.status == 200, f"Request {i+1} failed with status {response.status}"
        except urllib.error.HTTPError as e:
            pytest.fail(f"Request {i+1} failed with HTTP Error: {e.code}")
        except Exception as e:
            pytest.fail(f"Request {i+1} failed with Exception: {e}")

    # The 6th request should fail with 429 Too Many Requests
    req = urllib.request.Request(url, data=clean_payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            pytest.fail("6th request succeeded, but it should have been rate limited (429).")
    except urllib.error.HTTPError as e:
        assert e.code == 429, f"Expected 429 Too Many Requests on 6th request, got {e.code}"
    except Exception as e:
        pytest.fail(f"6th request failed with unexpected Exception: {e}")