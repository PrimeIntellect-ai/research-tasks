# test_final_state.py

import os
import glob
import subprocess
import json
import urllib.request
import urllib.error

def test_nginx_routing_audit():
    """Test that nginx correctly routes to the audit backend."""
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/api/audit/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"
    except Exception as e:
        assert False, f"Failed to connect to /api/audit/health via Nginx: {e}"

def test_nginx_routing_auth():
    """Test that nginx correctly routes to the auth service."""
    # We will just check if the endpoint is reachable and returns an HTTP response from the backend.
    # Without a valid token it might return 400/401, but it shouldn't return 502 Bad Gateway or 404 from nginx.
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/api/auth/verify")
        with urllib.request.urlopen(req, timeout=5) as response:
            # If it succeeds without a token, that's fine for routing check
            pass
    except urllib.error.HTTPError as e:
        # 400 or 401 means the request reached the auth service
        assert e.code in [200, 400, 401, 403], f"Expected auth service response, got HTTP {e.code}"
    except Exception as e:
        assert False, f"Failed to connect to /api/auth/verify via Nginx: {e}"

def test_detector_clean_corpus():
    """Test that the Rust detector correctly flags all clean files as CLEAN."""
    binary_path = "/home/user/detector/target/release/detector"
    assert os.path.isfile(binary_path), f"Detector binary not found at {binary_path}. Did you compile it?"
    assert os.access(binary_path, os.X_OK), f"Detector binary at {binary_path} is not executable."

    corpus_dir = "/app/corpus/clean/"
    files = glob.glob(os.path.join(corpus_dir, "*.json"))
    assert len(files) > 0, "Clean corpus is empty."

    try:
        result = subprocess.run([binary_path, corpus_dir], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        assert False, "Detector timed out on clean corpus."

    output = result.stdout.strip().split('\n')

    # Parse output: expected format "<filename>: CLEAN"
    results_map = {}
    for line in output:
        if not line.strip():
            continue
        parts = line.split(":")
        if len(parts) >= 2:
            filename = parts[0].strip()
            status = parts[1].strip()
            results_map[filename] = status

    failures = []
    for filepath in files:
        basename = os.path.basename(filepath)
        if basename not in results_map:
            failures.append(f"{basename} (missing output)")
        elif results_map[basename] != "CLEAN":
            failures.append(f"{basename} (flagged as {results_map[basename]})")

    if failures:
        assert False, f"{len(failures)} of {len(files)} clean modified (flagged incorrectly): {', '.join(failures)}"

def test_detector_evil_corpus():
    """Test that the Rust detector correctly flags all evil files as EVIL."""
    binary_path = "/home/user/detector/target/release/detector"
    assert os.path.isfile(binary_path), f"Detector binary not found at {binary_path}."

    corpus_dir = "/app/corpus/evil/"
    files = glob.glob(os.path.join(corpus_dir, "*.json"))
    assert len(files) > 0, "Evil corpus is empty."

    try:
        result = subprocess.run([binary_path, corpus_dir], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        assert False, "Detector timed out on evil corpus."

    output = result.stdout.strip().split('\n')

    # Parse output: expected format "<filename>: EVIL"
    results_map = {}
    for line in output:
        if not line.strip():
            continue
        parts = line.split(":")
        if len(parts) >= 2:
            filename = parts[0].strip()
            status = parts[1].strip()
            results_map[filename] = status

    failures = []
    for filepath in files:
        basename = os.path.basename(filepath)
        if basename not in results_map:
            failures.append(f"{basename} (missing output)")
        elif results_map[basename] != "EVIL":
            failures.append(f"{basename} (flagged as {results_map[basename]})")

    if failures:
        assert False, f"{len(failures)} of {len(files)} evil bypassed (flagged incorrectly): {', '.join(failures)}"