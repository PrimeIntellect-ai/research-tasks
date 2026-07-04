# test_final_state.py
import os
import subprocess
import urllib.request
import time
import pytest

def test_filter_script_corpus():
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists("/app/filter.sh"), "/app/filter.sh does not exist"
    assert os.access("/app/filter.sh", os.X_OK), "/app/filter.sh is not executable"

    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])
    evil_files = sorted([os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    clean_modified = []
    evil_bypassed = []

    for f in clean_files:
        res = subprocess.run(["/app/filter.sh", f], capture_output=True, text=True)
        if res.stdout.strip() != "ACCEPT":
            clean_modified.append(os.path.basename(f))

    for f in evil_files:
        res = subprocess.run(["/app/filter.sh", f], capture_output=True, text=True)
        if res.stdout.strip() != "REJECT":
            evil_bypassed.append(os.path.basename(f))

    err_msgs = []
    if evil_bypassed:
        err_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        err_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not err_msgs, " | ".join(err_msgs)

def test_pipeline_services_running():
    # Check if Redis is running on the correct port
    res = subprocess.run(["redis-cli", "-h", "127.0.0.1", "-p", "6379", "PING"], capture_output=True, text=True)
    assert "PONG" in res.stdout, "Redis server is not responding on 127.0.0.1:6379"

    # Check if Flask API is responding
    try:
        # Just checking if the port is open and responding to HTTP
        req = urllib.request.Request("http://127.0.0.1:8080/ingest", data=b"/dev/null", method="POST")
        response = urllib.request.urlopen(req, timeout=5)
        assert response.status in [200, 201, 202], f"API responded with unexpected status {response.status}"
    except urllib.error.HTTPError as e:
        # If the API returns a 400 or 500, it's at least running, but 200 is expected for a valid path
        pass
    except Exception as e:
        pytest.fail(f"Flask API is not reachable on 127.0.0.1:8080: {e}")

    # Verify the worker script is running
    res = subprocess.run(["pgrep", "-f", "worker.sh"], capture_output=True, text=True)
    assert res.stdout.strip() != "", "worker.sh daemon is not running in the background"