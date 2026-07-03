# test_final_state.py

import os
import sys
import json
import urllib.request
import urllib.error
import importlib.util
import pytest

def test_audit_complete_log():
    log_path = "/home/user/audit_complete.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "AUDIT FINISHED" in content, f"Log file {log_path} does not contain 'AUDIT FINISHED'."

def test_nginx_strips_internal_role():
    # Test 1: Request to Nginx with spoofed header should be blocked (403)
    req = urllib.request.Request("http://localhost:8080/api/admin")
    req.add_header("X-Internal-Role", "admin")

    try:
        response = urllib.request.urlopen(req)
        status = response.getcode()
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

    assert status == 403, f"Expected 403 Forbidden from Nginx for spoofed admin request, got {status}."

def test_flask_accepts_internal_role_directly():
    # Test 2: Direct request to Flask with header should succeed (200)
    req = urllib.request.Request("http://localhost:5000/api/admin")
    req.add_header("X-Internal-Role", "admin")

    try:
        response = urllib.request.urlopen(req)
        status = response.getcode()
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception as e:
        pytest.fail(f"Failed to connect to Flask on port 5000: {e}")

    assert status == 200, f"Expected 200 OK from Flask for direct admin request, got {status}."

def test_waf_filter_adversarial_corpus():
    waf_path = "/home/user/waf_filter.py"
    assert os.path.isfile(waf_path), f"WAF filter script {waf_path} is missing."

    # Dynamically import the waf_filter module
    spec = importlib.util.spec_from_file_location("waf_filter", waf_path)
    waf_filter = importlib.util.module_from_spec(spec)
    sys.modules["waf_filter"] = waf_filter
    try:
        spec.loader.exec_module(waf_filter)
    except Exception as e:
        pytest.fail(f"Failed to load {waf_path}: {e}")

    assert hasattr(waf_filter, "verify_request"), "verify_request function is missing in waf_filter.py."

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    evil_bypassed = []
    clean_modified = []

    # Test Evil Corpus
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
        headers = data.get("headers", {})
        cookies = data.get("cookies", {})
        try:
            result = waf_filter.verify_request(headers, cookies)
            if result is not False:
                evil_bypassed.append(filename)
        except Exception:
            # If it crashes on evil, we consider it not properly handled or rejected
            evil_bypassed.append(filename)

    # Test Clean Corpus
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
        headers = data.get("headers", {})
        cookies = data.get("cookies", {})
        try:
            result = waf_filter.verify_request(headers, cookies)
            if result is not True:
                clean_modified.append(filename)
        except Exception:
            clean_modified.append(filename)

    total_evil = len(evil_files)
    total_clean = len(clean_files)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {total_evil} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {total_clean} clean modified/rejected: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail("WAF filter failed corpus validation:\n" + "\n".join(error_msgs))