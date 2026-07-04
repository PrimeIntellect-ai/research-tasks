# test_final_state.py
import os
import sys
import json
import urllib.request
import urllib.error
import pytest

def test_sanitizer_corpus():
    sys.path.insert(0, '/home/user/app/gateway')
    try:
        from sanitizer import is_safe_payload
    except ImportError:
        pytest.fail("Could not import is_safe_payload from /home/user/app/gateway/sanitizer.py")

    clean_dir = '/home/user/app/corpora/clean'
    evil_dir = '/home/user/app/corpora/evil'

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]

    if not clean_files:
        pytest.fail(f"No clean files found in {clean_dir}")
    if not evil_files:
        pytest.fail(f"No evil files found in {evil_dir}")

    modified_clean = []
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        with open(path, 'r') as fp:
            content = fp.read()
        try:
            if not is_safe_payload(content):
                modified_clean.append(f)
        except Exception:
            modified_clean.append(f)

    bypassed_evil = []
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        with open(path, 'r') as fp:
            content = fp.read()
        try:
            if is_safe_payload(content):
                bypassed_evil.append(f)
        except Exception:
            # If it raises an exception, we can consider it rejected (or maybe it crashes, but let's assume crash means reject)
            pass

    error_msg = []
    if bypassed_evil:
        error_msg.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msg.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))


def test_e2e_clean_payload():
    url = "http://127.0.0.1:8080/api/v1/evaluate/test?x=2.0"
    payload = {"type": "polynomial", "coefficients": [1.0, 2.0, 3.0], "depth": 1}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            resp_body = response.read().decode('utf-8')
            resp_json = json.loads(resp_body)
            assert "result" in resp_json, "Response missing 'result' key"
            assert abs(resp_json["result"] - 17.0) < 1e-6, f"Expected result 17.0, got {resp_json['result']}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTPError on clean payload: {e.code} {e.reason}")
    except Exception as e:
        pytest.fail(f"Exception during clean payload E2E test: {e}")


def test_e2e_evil_payload():
    url = "http://127.0.0.1:8080/api/v1/evaluate/test?x=2.0"
    # Create an evil payload (depth > 10)
    payload = {"type": "polynomial", "coefficients": [1.0], "depth": 11}
    # Deeply nested to trigger depth check
    curr = payload
    for _ in range(15):
        curr["child"] = {}
        curr = curr["child"]

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            pytest.fail(f"Expected 400 Bad Request for evil payload, got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected 400 Bad Request, got {e.code}"
    except Exception as e:
        pytest.fail(f"Exception during evil payload E2E test: {e}")