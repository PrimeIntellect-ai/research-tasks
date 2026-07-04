# test_final_state.py

import os
import subprocess
import time
import urllib.request
import pytest

def test_client_certs_exist():
    assert os.path.isfile("/app/certs/client.crt"), "/app/certs/client.crt is missing. You must generate a client certificate."
    assert os.path.isfile("/app/certs/client.key"), "/app/certs/client.key is missing. You must generate a client private key."

def test_nginx_mtls_health():
    """
    Ensures that the healthcheck endpoint is reachable and returns 200 OK.
    If it's not reachable initially, we attempt to run the start.sh script.
    """
    url = "http://127.0.0.1:8080/health"

    def check_health():
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.getcode(), response.read().decode('utf-8')
        except Exception:
            return None, None

    code, body = check_health()
    if code is None:
        # Services might not be running, try starting them
        subprocess.Popen(["/app/start.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Poll for up to 5 seconds
        for _ in range(10):
            time.sleep(0.5)
            code, body = check_health()
            if code is not None:
                break

    assert code is not None, f"Could not reach {url}. Services failed to start or Nginx is misconfigured."
    assert code == 200, f"Expected HTTP 200 from {url}, got {code}. Check mTLS Nginx configuration."
    assert '{"status": "ok"}' in body, f"Unexpected response body: {body}"

def test_classifier_exists():
    assert os.path.isfile("/app/classifier"), "/app/classifier executable is missing. Did you compile your Go program?"
    assert os.access("/app/classifier", os.X_OK), "/app/classifier is not executable."

def test_classifier_clean_corpus():
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"{clean_dir} missing"
    clean_files = os.listdir(clean_dir)
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed = []
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        with open(path, "r") as fp:
            payload = fp.read().strip()

        res = subprocess.run(["/app/classifier", payload], capture_output=True)
        if res.returncode != 0:
            failed.append(f)

    assert not failed, f"{len(failed)} of {len(clean_files)} clean modified/rejected. Offending: {failed}"

def test_classifier_evil_corpus():
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"{evil_dir} missing"
    evil_files = os.listdir(evil_dir)
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed = []
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        with open(path, "r") as fp:
            payload = fp.read().strip()

        res = subprocess.run(["/app/classifier", payload], capture_output=True)
        if res.returncode != 1:
            failed.append(f)

    assert not failed, f"{len(failed)} of {len(evil_files)} evil bypassed. Offending: {failed}"