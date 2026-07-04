# test_final_state.py

import os
import json
import subprocess
import tempfile
import urllib.request
import urllib.error
import pytest

# Paths
ENV_FILE = "/app/.env"
NGINX_CONF = "/app/nginx/nginx.conf"
VALIDATE_SCRIPT = "/home/user/validate_loc.py"
CLEAN_CORPUS_DIR = "/app/data/clean/"
EVIL_CORPUS_DIR = "/app/data/evil/"
INGEST_URL = "http://localhost:8080/ingest"

@pytest.fixture(scope="session", autouse=True)
def restart_services():
    """Ensure services are restarted with the new configurations before testing endpoints."""
    restart_script = "/app/restart_services.sh"
    if os.path.isfile(restart_script) and os.access(restart_script, os.X_OK):
        subprocess.run([restart_script], check=False)

def test_env_configuration():
    """Check that REDIS_HOST is set to 127.0.0.1 in the .env file."""
    assert os.path.isfile(ENV_FILE), f"{ENV_FILE} is missing."
    with open(ENV_FILE, "r") as f:
        content = f.read()

    # Check for REDIS_HOST=127.0.0.1
    found = any(line.strip() == "REDIS_HOST=127.0.0.1" for line in content.splitlines())
    assert found, f"REDIS_HOST is not set to 127.0.0.1 in {ENV_FILE}"

def test_nginx_configuration():
    """Check that nginx.conf is proxying to the Flask API."""
    assert os.path.isfile(NGINX_CONF), f"{NGINX_CONF} is missing."
    with open(NGINX_CONF, "r") as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:5000" in content or "proxy_pass http://localhost:5000" in content, \
        f"Nginx configuration does not properly proxy to http://127.0.0.1:5000 in {NGINX_CONF}"

def test_validate_loc_script_exists():
    """Ensure the validation script exists."""
    assert os.path.isfile(VALIDATE_SCRIPT), f"Validation script missing at {VALIDATE_SCRIPT}"

def test_validate_loc_corpus_direct():
    """Test the validation script directly against the clean and evil corpora."""
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus missing at {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus missing at {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    evil_bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test Clean Corpus
        for c_file in clean_files:
            out_file = os.path.join(tmpdir, "out_" + os.path.basename(c_file) + ".json")
            result = subprocess.run(
                ["python3", VALIDATE_SCRIPT, c_file, out_file],
                capture_output=True, text=True
            )

            if result.returncode != 0:
                clean_failed.append(os.path.basename(c_file))
                continue

            if not os.path.isfile(out_file):
                clean_failed.append(os.path.basename(c_file))
                continue

            try:
                with open(out_file, "r") as f:
                    json.load(f)
            except ValueError:
                clean_failed.append(os.path.basename(c_file))

        # Test Evil Corpus
        for e_file in evil_files:
            out_file = os.path.join(tmpdir, "out_" + os.path.basename(e_file) + ".json")
            result = subprocess.run(
                ["python3", VALIDATE_SCRIPT, e_file, out_file],
                capture_output=True, text=True
            )

            if result.returncode == 0:
                evil_bypassed.append(os.path.basename(e_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    assert not evil_bypassed and not clean_failed, " | ".join(error_msgs)

def post_multipart_file(url, file_path):
    """Helper to post a file as multipart/form-data using stdlib."""
    import uuid
    boundary = uuid.uuid4().hex

    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        file_content = f.read()

    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode('utf-8') + file_content + f"\r\n--{boundary}--\r\n".encode('utf-8')

    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    try:
        with urllib.request.urlopen(req) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError:
        return None

def test_http_endpoint_corpus():
    """Test the Nginx -> Flask pipeline with the clean and evil corpora."""
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    clean_failed = []
    evil_bypassed = []

    for c_file in clean_files:
        status = post_multipart_file(INGEST_URL, c_file)
        if status != 200:
            clean_failed.append(f"{os.path.basename(c_file)} (status {status})")

    for e_file in evil_files:
        status = post_multipart_file(INGEST_URL, e_file)
        if status != 400:
            evil_bypassed.append(f"{os.path.basename(e_file)} (status {status})")

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed HTTP checks: {', '.join(evil_bypassed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean rejected by HTTP checks: {', '.join(clean_failed)}")

    assert not evil_bypassed and not clean_failed, " | ".join(error_msgs)