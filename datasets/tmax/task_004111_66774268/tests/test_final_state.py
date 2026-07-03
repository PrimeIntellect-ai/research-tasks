# test_final_state.py

import os
import glob
import subprocess
import urllib.request
import urllib.error
import json
import pytest

def test_nginx_configuration():
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Nginx config not found at {nginx_conf_path}"
    with open(nginx_conf_path, "r") as f:
        content = f.read()

    assert "proxy_pass" in content, "Nginx config is missing proxy_pass directive."
    assert "http://127.0.0.1:5000" in content or "http://localhost:5000" in content, \
        "Nginx config does not properly proxy to Flask app on port 5000."

def test_flask_environment_variables():
    run_flask_path = "/home/user/app/run_flask.sh"
    assert os.path.isfile(run_flask_path), f"Flask run script not found at {run_flask_path}"
    with open(run_flask_path, "r") as f:
        content = f.read()

    assert "POSTGRES_URI" in content, "POSTGRES_URI not set in run_flask.sh"
    assert "MONGO_URI" in content, "MONGO_URI not set in run_flask.sh"
    assert "127.0.0.1:5432" in content or "localhost:5432" in content, "PostgreSQL port/host missing"
    assert "biomed" in content, "PostgreSQL database name 'biomed' missing"
    assert "researcher" in content, "PostgreSQL user missing"
    assert "secret" in content, "PostgreSQL password missing"
    assert "127.0.0.1:27017" in content or "localhost:27017" in content, "MongoDB port/host missing"
    assert "biomed_notes" in content, "MongoDB database 'biomed_notes' missing"

def test_end_to_end_proxy():
    # Attempt to hit the Nginx proxy endpoint.
    # Even if the DBs aren't fully populated, it should reach Flask and return a response (e.g. 200 or 400/500 if payload is bad, but not 502 Bad Gateway).
    url = "http://127.0.0.1:8080/query"
    payload = json.dumps({
        "sql_relations": ["patients"],
        "join_conditions": [],
        "mongo_filter": {},
        "cross_map": ""
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        response = urllib.request.urlopen(req, timeout=5)
        assert response.status in [200, 400, 500], f"Unexpected status code {response.status}"
    except urllib.error.HTTPError as e:
        # If Flask returns an error, it means the proxy works. 502 means proxy failed.
        assert e.code != 502, "Nginx returned 502 Bad Gateway. Nginx to Flask proxying is failing."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

def test_cross_join_detector_script_exists():
    script_path = "/home/user/detect_cross_join.py"
    assert os.path.isfile(script_path), f"Detector script not found at {script_path}"

def test_adversarial_corpus_evil():
    script_path = "/home/user/detect_cross_join.py"
    evil_dir = "/home/user/corpora/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", script_path, filepath],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "REJECT":
            bypassed.append(os.path.basename(filepath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_adversarial_corpus_clean():
    script_path = "/home/user/detect_cross_join.py"
    clean_dir = "/home/user/corpora/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, "No clean corpus files found."

    modified = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", script_path, filepath],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "ACCEPT":
            modified.append(os.path.basename(filepath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected: {', '.join(modified)}")