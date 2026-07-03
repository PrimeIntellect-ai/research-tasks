# test_final_state.py

import os
import json
import subprocess
import tempfile
import time
import urllib.request
import urllib.error
import pytest

def test_detector_evil_corpus():
    evil_dir = "/home/user/corpora/evil"
    detector_script = "/home/user/detector.py"

    assert os.path.exists(detector_script), f"Detector script not found at {detector_script}"

    bypassed = []

    for filename in os.listdir(evil_dir):
        if not filename.endswith(".jsonl"): 
            continue
        in_path = os.path.join(evil_dir, filename)
        out_path = tempfile.mktemp(suffix=".jsonl")

        try:
            subprocess.run(["python3", detector_script, in_path, out_path], check=True, capture_output=True, text=True)

            with open(out_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    if not data.get("leak"):
                        bypassed.append(f"{filename} id {data.get('id')}")
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    assert not bypassed, f"{len(bypassed)} evil bypassed: {bypassed}"

def test_detector_clean_corpus():
    clean_dir = "/home/user/corpora/clean"
    detector_script = "/home/user/detector.py"

    assert os.path.exists(detector_script), f"Detector script not found at {detector_script}"

    modified = []

    for filename in os.listdir(clean_dir):
        if not filename.endswith(".jsonl"): 
            continue
        in_path = os.path.join(clean_dir, filename)
        out_path = tempfile.mktemp(suffix=".jsonl")

        try:
            subprocess.run(["python3", detector_script, in_path, out_path], check=True, capture_output=True, text=True)

            with open(out_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    if data.get("leak"):
                        modified.append(f"{filename} id {data.get('id')}")
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    assert not modified, f"{len(modified)} clean modified: {modified}"

def test_api_code_patched():
    api_path = "/home/user/app/api.py"
    assert os.path.exists(api_path), "api.py not found"

    with open(api_path, "r") as f:
        api_code = f.read()

    assert "0.0.0.0" not in api_code, "api.py still binds to 0.0.0.0"
    assert "127.0.0.1" in api_code, "api.py does not bind to 127.0.0.1"
    assert "env=" in api_code or "os.environ" in api_code, "api.py does not seem to pass environment variables to the worker"

def test_worker_code_patched():
    worker_path = "/home/user/app/worker.py"
    assert os.path.exists(worker_path), "worker.py not found"

    with open(worker_path, "r") as f:
        worker_code = f.read()

    assert "os.environ" in worker_code or "environ.get" in worker_code, "worker.py does not read from environment variables"

def test_end_to_end_flow():
    start_script = "/home/user/app/start.sh"
    assert os.path.exists(start_script), "start.sh not found"

    # Ensure any previous instances are dead
    subprocess.run(["pkill", "-f", "nginx"], check=False)
    subprocess.run(["pkill", "-f", "api.py"], check=False)
    time.sleep(1)

    # Start the app
    subprocess.run(["bash", start_script], check=True)
    time.sleep(3)

    try:
        # Send POST request
        req = urllib.request.Request(
            "http://127.0.0.1:8080/process",
            data=json.dumps({"secret": "test1234"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req) as response:
                assert response.status == 200, f"Expected 200 OK, got {response.status}"
                res_data = json.loads(response.read().decode("utf-8"))
                assert res_data.get("worker_output") == "Processed_test***", f"Worker output is incorrect: {res_data}"
        except urllib.error.URLError as e:
            pytest.fail(f"Request failed: {e}")

        # Check socket bindings
        ss_out = subprocess.run(["ss", "-tln"], capture_output=True, text=True).stdout
        assert "0.0.0.0:5000" not in ss_out, "Port 5000 is still bound to 0.0.0.0"
        assert "*:5000" not in ss_out, "Port 5000 is still bound to all interfaces"

    finally:
        # Clean up
        subprocess.run(["pkill", "-f", "nginx"], check=False)
        subprocess.run(["pkill", "-f", "api.py"], check=False)