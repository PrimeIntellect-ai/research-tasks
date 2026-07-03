# test_final_state.py
import os
import subprocess
import urllib.request
import json
import pytest

def test_service_topology_health():
    """
    Test that the Nginx reverse proxy correctly routes to the Backup API,
    and the API successfully connects to Postgres and Redis to report healthy.
    """
    try:
        req = urllib.request.Request("http://localhost:8080/api/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}"
            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                pytest.fail(f"Expected JSON response, got: {body}")

            assert data.get("status") == "healthy", f"Expected {{'status': 'healthy'}}, got {data}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to health endpoint: {e}. Check nginx.conf and backend/.env configuration.")

def test_sanitizer_adversarial_corpus():
    """
    Test the compiled sanitizer binary against the clean and evil corpora.
    """
    sanitizer_bin = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_bin), f"Sanitizer binary not found at {sanitizer_bin}. Did you compile it?"
    assert os.access(sanitizer_bin, os.X_OK), f"Sanitizer binary at {sanitizer_bin} is not executable."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')])
    evil_files = sorted([os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')])

    clean_modified = []
    evil_bypassed = []

    # Check clean corpus
    for cf in clean_files:
        with open(cf, 'rb') as f:
            result = subprocess.run([sanitizer_bin], stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8').strip()
            if result.returncode != 0 or output != "ACCEPT":
                clean_modified.append(os.path.basename(cf))

    # Check evil corpus
    for ef in evil_files:
        with open(ef, 'rb') as f:
            result = subprocess.run([sanitizer_bin], stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8').strip()
            if result.returncode != 0 or output != "REJECT":
                evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))