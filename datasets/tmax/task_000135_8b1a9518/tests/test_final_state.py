# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import time
import pytest

VALIDATOR_PATH = "/home/user/elf_validator"
EVIL_CORPUS = "/app/corpus/evil/"
CLEAN_CORPUS = "/app/corpus/clean/"
NGINX_CONF = "/app/nginx/nginx.conf"

def test_elf_validator_exists_and_executable():
    assert os.path.isfile(VALIDATOR_PATH), f"Validator binary not found at {VALIDATOR_PATH}"
    assert os.access(VALIDATOR_PATH, os.X_OK), f"Validator binary at {VALIDATOR_PATH} is not executable"

def test_corpus_evaluation():
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]

    assert len(evil_files) > 0, "No files found in evil corpus"
    assert len(clean_files) > 0, "No files found in clean corpus"

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run([VALIDATOR_PATH, ef], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    clean_modified = []
    for cf in clean_files:
        result = subprocess.run([VALIDATOR_PATH, cf], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    if error_msg:
        pytest.fail("Corpus evaluation failed. " + " | ".join(error_msg))

def test_nginx_config_updated():
    with open(NGINX_CONF, 'r') as f:
        content = f.read()

    assert "Content-Security-Policy" in content, "CSP header missing in Nginx config"
    assert "default-src 'none'" in content and "frame-ancestors 'none'" in content, "CSP header values are incorrect"
    assert "proxy_pass http://127.0.0.1:9090" in content.replace(" ", "").replace("\t", "").replace("proxy_passhttp://127.0.0.1:9090", "proxy_pass http://127.0.0.1:9090"), "proxy_pass to backend missing in Nginx config"

def test_end_to_end_flow():
    # Start services if they aren't already running
    subprocess.run(["/app/start_services.sh"], check=False)
    time.sleep(2)  # Give services a moment to start

    clean_sample = os.path.join(CLEAN_CORPUS, os.listdir(CLEAN_CORPUS)[0])
    evil_sample = os.path.join(EVIL_CORPUS, os.listdir(EVIL_CORPUS)[0])

    with open(clean_sample, 'rb') as f:
        clean_data = f.read()
    with open(evil_sample, 'rb') as f:
        evil_data = f.read()

    req_clean = urllib.request.Request("http://127.0.0.1:8080/upload", data=clean_data, method="POST")
    try:
        with urllib.request.urlopen(req_clean, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 for clean binary, got {response.status}"
            csp = response.getheader("Content-Security-Policy")
            assert csp is not None, "Content-Security-Policy header is missing in response"
            assert "default-src 'none'" in csp and "frame-ancestors 'none'" in csp, "CSP header in response is incorrect"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200 for clean binary, got {e.code}")
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx for clean binary: {e}")

    req_evil = urllib.request.Request("http://127.0.0.1:8080/upload", data=evil_data, method="POST")
    try:
        with urllib.request.urlopen(req_evil, timeout=5) as response:
            pytest.fail(f"Expected HTTP 400 for evil binary, got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400 for evil binary, got {e.code}"
        csp = e.headers.get("Content-Security-Policy")
        assert csp is not None, "Content-Security-Policy header is missing in 400 response"
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx for evil binary: {e}")

    # Check Redis for audit logs
    try:
        redis_result = subprocess.run(["redis-cli", "dbsize"], capture_output=True, text=True, timeout=3)
        assert redis_result.returncode == 0, "Failed to connect to Redis"
        keys_count = int(redis_result.stdout.strip().split('\n')[-1])
        assert keys_count > 0, "No audit logs found in Redis"
    except Exception as e:
        pytest.fail(f"Redis validation failed: {e}")