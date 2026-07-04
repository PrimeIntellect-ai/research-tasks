# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import json
import pytest

def test_cypher_sanitizer_exists():
    binary_path = "/home/user/app/cypher_sanitizer"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_adversarial_corpus():
    binary_path = "/home/user/app/cypher_sanitizer"
    evil_dir = "/home/user/corpora/evil/"
    clean_dir = "/home/user/corpora/clean/"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.cypher')]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.cypher')]

    evil_bypassed = []
    clean_modified = []

    for ef in evil_files:
        filepath = os.path.join(evil_dir, ef)
        with open(filepath, 'rb') as f:
            query_bytes = f.read()

        result = subprocess.run([binary_path], input=query_bytes, capture_output=True)
        stdout = result.stdout.decode('utf-8').strip()

        if result.returncode != 1 or stdout != "EVIL":
            evil_bypassed.append(ef)

    for cf in clean_files:
        filepath = os.path.join(clean_dir, cf)
        with open(filepath, 'rb') as f:
            query_bytes = f.read()

        result = subprocess.run([binary_path], input=query_bytes, capture_output=True)
        stdout = result.stdout.decode('utf-8').strip()

        if result.returncode != 0 or stdout != "CLEAN":
            clean_modified.append(cf)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)

def test_service_configuration():
    nginx_conf_path = "/home/user/app/nginx.conf"
    env_path = "/home/user/app/.env"

    assert os.path.isfile(nginx_conf_path), f"{nginx_conf_path} is missing."
    with open(nginx_conf_path, "r") as f:
        nginx_content = f.read()
    assert "127.0.0.1:5000" in nginx_content or "localhost:5000" in nginx_content, "Nginx configuration does not route to Flask API on port 5000."

    assert os.path.isfile(env_path), f"{env_path} is missing."
    with open(env_path, "r") as f:
        env_content = f.read()
    assert "127.0.0.1:7687" in env_content or "localhost:7687" in env_content, "Flask .env does not configure GRAPH_DB_URL to port 7687."

def test_end_to_end_flow():
    script_path = "/home/user/app/start_services.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."

    # Start the services
    subprocess.run(["bash", script_path], check=False)

    # Wait for services to be ready
    time.sleep(3)

    url = "http://127.0.0.1:8080/query"
    data = json.dumps({"query": "MATCH (n) RETURN n LIMIT 1"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 OK, got {response.status}"
            body = response.read().decode("utf-8")
            assert body, "Response body should not be empty."
    except urllib.error.URLError as e:
        pytest.fail(f"End-to-end flow failed: {e}")