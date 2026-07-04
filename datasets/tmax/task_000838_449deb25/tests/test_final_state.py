# test_final_state.py

import os
import time
import json
import subprocess
import urllib.request
import urllib.error
import pytest

@pytest.fixture(scope="module", autouse=True)
def setup_services():
    """Start all services using the provided script and wait for them to be ready."""
    script_path = "/app/start_all.sh"
    if os.path.exists(script_path):
        subprocess.run(["bash", script_path], check=False)
        # Wait for services to come up
        time.sleep(3)
    yield
    # Teardown: kill processes if needed, but usually the container will just exit.
    subprocess.run(["pkill", "-f", "nginx"], check=False)
    subprocess.run(["pkill", "-f", "gunicorn"], check=False)
    subprocess.run(["pkill", "-f", "redis-server"], check=False)

def test_nginx_config_updated():
    path = "/app/nginx/nginx.conf"
    assert os.path.isfile(path), f"Missing Nginx config: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "127.0.0.1:5000" in content, "Nginx config does not proxy to 127.0.0.1:5000"
    assert "/intake" in content, "Nginx config missing /intake location"

def test_flask_env_updated():
    path = "/app/flask/.env"
    assert os.path.isfile(path), f"Missing Flask env file: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "REDIS_HOST=127.0.0.1" in content, "Flask .env missing REDIS_HOST=127.0.0.1"
    assert "REDIS_PORT=6379" in content, "Flask .env missing REDIS_PORT=6379"

def send_payload(url, filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=5)
        return response.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return None

def test_clean_corpus_accepted():
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        status = send_payload("http://127.0.0.1:8080/intake", filepath)
        if status != 200:
            failed_files.append((filename, status))

    if failed_files:
        failures = ", ".join([f"{f} (status {s})" for f, s in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {failures}")

def test_evil_corpus_rejected():
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        status = send_payload("http://127.0.0.1:8080/intake", filepath)
        if status != 400:
            failed_files.append((filename, status))

    if failed_files:
        failures = ", ".join([f"{f} (status {s})" for f, s in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {failures}")