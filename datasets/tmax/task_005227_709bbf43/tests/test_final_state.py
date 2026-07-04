# test_final_state.py

import os
import json
import time
import urllib.request
import subprocess
import pytest

def test_pipeline_id_extracted():
    path = "/home/user/pipeline_id.txt"
    assert os.path.isfile(path), f"Missing pipeline_id.txt at {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "A8F93X7", f"Expected pipeline ID 'A8F93X7', but got '{content}'"

def test_linter_script():
    linter_path = "/home/user/linter.sh"
    assert os.path.isfile(linter_path), f"Missing linter script at {linter_path}"
    assert os.access(linter_path, os.X_OK), f"Linter script {linter_path} is not executable"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".build")]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".build")]

    clean_failed = []
    for f in clean_files:
        res = subprocess.run(["bash", linter_path, f])
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        res = subprocess.run(["bash", linter_path, f])
        if res.returncode != 1:
            evil_failed.append(os.path.basename(f))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_failed)}")

    assert not error_msgs, "Linter validation failed:\n" + "\n".join(error_msgs)

def test_api_script():
    api_path = "/home/user/api.sh"
    assert os.path.isfile(api_path), f"Missing API script at {api_path}"
    assert os.access(api_path, os.X_OK), f"API script {api_path} is not executable"

    # Start the API server
    proc = subprocess.Popen(["bash", api_path])

    response_data = None
    try:
        # Wait for the server to start
        for _ in range(10):
            try:
                req = urllib.request.Request("http://localhost:8080/dependencies")
                with urllib.request.urlopen(req, timeout=2) as response:
                    assert response.status == 200, f"Expected HTTP 200, got {response.status}"
                    response_data = response.read().decode("utf-8")
                    break
            except Exception:
                time.sleep(1)
        else:
            pytest.fail("Failed to connect to API server on port 8080 after 10 seconds")
    finally:
        proc.terminate()
        proc.wait(timeout=5)

    assert response_data is not None, "Did not receive response from API"

    try:
        graph = json.loads(response_data)
    except json.JSONDecodeError:
        pytest.fail(f"API response is not valid JSON: {response_data}")

    expected_graph = {
        "app": ["utils", "core"],
        "utils": [],
        "core": ["utils"]
    }

    # Convert lists to sets for order-independent comparison
    actual_graph_sets = {k: set(v) for k, v in graph.items()}
    expected_graph_sets = {k: set(v) for k, v in expected_graph.items()}

    assert actual_graph_sets == expected_graph_sets, f"Dependency graph mismatch. Expected {expected_graph}, got {graph}"