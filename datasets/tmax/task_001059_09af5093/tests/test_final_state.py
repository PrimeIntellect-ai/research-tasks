# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import subprocess
import pytest

def test_nginx_routing_health():
    """Test that Nginx routes /api/health to Flask correctly."""
    url = "http://127.0.0.1:8080/api/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

def test_flask_uses_backup_db():
    """Test that Flask API uses the backup.db instead of prod.db."""
    app_py_path = "/home/user/api/app.py"
    assert os.path.isfile(app_py_path), f"Flask app file missing at {app_py_path}"
    with open(app_py_path, 'r') as f:
        content = f.read()

    assert "backup.db" in content, "The Flask app does not appear to be updated to use backup.db."
    assert "prod.db" not in content or content.index("backup.db") > -1, "The Flask app still uses prod.db."

def test_exported_graph():
    """Test that the exported graph JSON exists and has correct format."""
    export_path = "/home/user/exported_graph.json"
    assert os.path.isfile(export_path), f"Expected exported graph at {export_path} is missing."

    with open(export_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Exported graph is not a valid JSON file.")

    assert isinstance(data, list), "Exported graph JSON should be a list of dictionaries."
    if len(data) > 0:
        for item in data:
            assert isinstance(item, dict), "Items in exported graph list must be dictionaries."
            assert "parent" in item, "Missing 'parent' key in exported graph item."
            assert "child" in item, "Missing 'child' key in exported graph item."

def test_detect_corruption_evil_corpus():
    """Test that the detect_corruption script correctly identifies evil (cyclic) graphs."""
    script_path = "/home/user/detect_corruption.py"
    evil_dir = "/app/corpora/evil/"

    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    result = subprocess.run(["python3", script_path, evil_dir], capture_output=True, text=True)
    output = result.stdout.strip()

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    bypassed = []

    for f in evil_files:
        expected_str = f"{f}: EVIL"
        if expected_str not in output:
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_detect_corruption_clean_corpus():
    """Test that the detect_corruption script correctly identifies clean (DAG) graphs."""
    script_path = "/home/user/detect_corruption.py"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    result = subprocess.run(["python3", script_path, clean_dir], capture_output=True, text=True)
    output = result.stdout.strip()

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    modified = []

    for f in clean_files:
        expected_str = f"{f}: CLEAN"
        if expected_str not in output:
            modified.append(f)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(modified)}")