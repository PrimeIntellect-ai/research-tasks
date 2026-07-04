# test_final_state.py
import os
import json
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_services_running():
    """Verify that Nginx, Redis, Flask, and Celery are running."""
    # Check Redis
    try:
        subprocess.check_output(["redis-cli", "ping"])
    except subprocess.CalledProcessError:
        pytest.fail("Redis is not running or not responding to ping.")

    # Check Nginx
    try:
        output = subprocess.check_output(["ps", "aux"]).decode()
        assert "nginx" in output, "Nginx process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check processes for Nginx.")

    # Check Flask and Celery (basic process check)
    assert "api.py" in output or "flask" in output or "gunicorn" in output, "Flask API process is not running."
    assert "celery" in output, "Celery worker process is not running."

def test_end_to_end_simulation():
    """Verify that the Nginx proxy correctly routes to Flask and Celery processes the task."""
    payload = json.dumps({"sequence": "ATGC"}).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:8080/simulate",
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    try:
        response = urllib.request.urlopen(req, timeout=10)
        assert response.status in [200, 202], f"Expected HTTP 200/202, got {response.status}"
        data = json.loads(response.read().decode())
        # The exact response depends on the dummy app, but we expect it to not fail.
        assert data is not None
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or task failed: {e}")

def parse_fasta(file_path):
    """Helper to parse FASTA file and return a list of sequence IDs."""
    seq_ids = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                seq_ids.append(line[1:].strip())
    return seq_ids

def test_classifier_clean_corpus():
    """Verify classifier accepts 100% of clean sequences."""
    script_path = "/home/user/app/classifier.py"
    corpus_path = "/home/user/data/clean_sequences.fasta"

    assert os.path.exists(script_path), f"Classifier script not found at {script_path}"

    # Run classifier
    try:
        subprocess.run(["python3", script_path, corpus_path], check=True, cwd="/home/user/app")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Classifier script failed on clean corpus: {e}")

    json_path = "/home/user/app/classifications.json"
    assert os.path.exists(json_path), "classifications.json was not generated."

    with open(json_path, 'r') as f:
        classifications = json.load(f)

    seq_ids = parse_fasta(corpus_path)
    rejected = []
    for seq_id in seq_ids:
        if classifications.get(seq_id) != "accept":
            rejected.append(seq_id)

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(seq_ids)} clean modified/rejected. Offending IDs: {rejected[:5]}...")

def test_classifier_evil_corpus():
    """Verify classifier rejects 100% of evil sequences."""
    script_path = "/home/user/app/classifier.py"
    corpus_path = "/home/user/data/evil_sequences.fasta"

    # Run classifier
    try:
        subprocess.run(["python3", script_path, corpus_path], check=True, cwd="/home/user/app")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Classifier script failed on evil corpus: {e}")

    json_path = "/home/user/app/classifications.json"
    assert os.path.exists(json_path), "classifications.json was not generated."

    with open(json_path, 'r') as f:
        classifications = json.load(f)

    seq_ids = parse_fasta(corpus_path)
    bypassed = []
    for seq_id in seq_ids:
        if classifications.get(seq_id) != "reject":
            bypassed.append(seq_id)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(seq_ids)} evil bypassed. Offending IDs: {bypassed[:5]}...")

def test_orchestrate_notebook_exists():
    """Verify the Jupyter notebook orchestrate.ipynb exists."""
    assert os.path.isfile("/home/user/app/orchestrate.ipynb"), "/home/user/app/orchestrate.ipynb is missing."