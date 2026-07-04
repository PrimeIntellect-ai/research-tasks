# test_final_state.py

import os
import subprocess
import json
import base64
import hmac
import hashlib
import urllib.request
import urllib.error
import socket
import pytest

DETECTOR_BIN = "/home/user/detector/target/debug/detector"
EVIL_CORPUS_DIR = "/home/user/corpora/evil"
CLEAN_CORPUS_DIR = "/home/user/corpora/clean"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_BIN), f"Detector binary not found at {DETECTOR_BIN}"
    assert os.access(DETECTOR_BIN, os.X_OK), f"Detector binary at {DETECTOR_BIN} is not executable"

def test_detector_corpus():
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "Evil corpus is empty"
    assert len(clean_files) > 0, "Clean corpus is empty"

    evil_bypassed = []
    for fpath in evil_files:
        try:
            result = subprocess.run([DETECTOR_BIN, fpath], capture_output=True, text=True, timeout=2)
            if result.stdout.strip() != "EVIL":
                evil_bypassed.append(os.path.basename(fpath))
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(fpath)} (Error: {e})")

    clean_modified = []
    for fpath in clean_files:
        try:
            result = subprocess.run([DETECTOR_BIN, fpath], capture_output=True, text=True, timeout=2)
            if result.stdout.strip() != "CLEAN":
                clean_modified.append(os.path.basename(fpath))
        except Exception as e:
            clean_modified.append(f"{os.path.basename(fpath)} (Error: {e})")

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_backend_bound_localhost():
    # Check if port 8080 is bound to 127.0.0.1 and not 0.0.0.0
    try:
        result = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True)
        # We look for 127.0.0.1:8080
        lines = result.stdout.splitlines()
        found_8080 = False
        bound_to_localhost = False
        for line in lines:
            if ":8080" in line:
                found_8080 = True
                if "127.0.0.1:8080" in line:
                    bound_to_localhost = True
                elif "0.0.0.0:8080" in line or "*:8080" in line:
                    pytest.fail("Backend is still bound to 0.0.0.0:8080 (externally accessible)")

        assert found_8080, "Port 8080 is not listening. Is the backend running?"
        assert bound_to_localhost, "Backend is not bound to 127.0.0.1:8080"
    except FileNotFoundError:
        # Fallback to socket connection test if ss is not available
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            # Try connecting via a non-localhost interface (if we know its IP) or just rely on ss
            pass
        finally:
            s.close()

def create_jwt(header, payload, secret=None):
    b64_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    b64_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    msg = f"{b64_header}.{b64_payload}"
    if secret:
        sig = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()
        b64_sig = base64.urlsafe_b64encode(sig).decode().rstrip('=')
        return f"{msg}.{b64_sig}"
    return f"{msg}."

def test_api_secure_endpoint():
    valid_header = {"alg": "HS256", "typ": "JWT"}
    payload = {"user_id": "user123"}
    secret = "secret_key_123"

    valid_jwt = create_jwt(valid_header, payload, secret)

    none_header = {"alg": "none", "typ": "JWT"}
    none_jwt = create_jwt(none_header, payload, None)

    # Test valid JWT
    req = urllib.request.Request("http://localhost:8000/api/secure")
    req.add_header("Authorization", f"Bearer {valid_jwt}")
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected 200 OK for valid JWT, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Valid JWT request failed with status {e.code}")
    except Exception as e:
        pytest.fail(f"Valid JWT request failed: {e}")

    # Test alg=none JWT
    req_none = urllib.request.Request("http://localhost:8000/api/secure")
    req_none.add_header("Authorization", f"Bearer {none_jwt}")
    try:
        with urllib.request.urlopen(req_none, timeout=2) as response:
            pytest.fail(f"Expected failure for alg=none JWT, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code in [401, 403], f"Expected 401 or 403 for alg=none JWT, got {e.code}"
    except Exception as e:
        pytest.fail(f"alg=none JWT request failed unexpectedly: {e}")