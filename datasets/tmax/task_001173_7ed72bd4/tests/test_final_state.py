# test_final_state.py

import os
import subprocess
import time
import json
import urllib.request
import urllib.error
import socket

def test_files_exist():
    """Verify that all required files and directories were created."""
    assert os.path.isdir("/home/user/workspace"), "/home/user/workspace directory is missing."
    assert os.path.isdir("/home/user/venv"), "/home/user/venv directory is missing."

    expected_files = [
        "/home/user/workspace/requirements.txt",
        "/home/user/workspace/dag.py",
        "/home/user/workspace/app.py",
        "/home/user/workspace/test_app.py",
        "/home/user/start_server.sh"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"File {f} is missing."

def test_agent_tests_pass():
    """Run the student's test suite and ensure it passes."""
    cmd = "source /home/user/venv/bin/activate && pytest /home/user/workspace/test_app.py"
    result = subprocess.run(cmd, shell=True, executable="/bin/bash", capture_output=True, text=True)
    assert result.returncode == 0, f"Agent tests failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def wait_for_port(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

def test_api_behavior():
    """Start the server and test the API endpoints."""
    # Ensure script is executable
    os.chmod("/home/user/start_server.sh", 0o755)

    # Start the server
    subprocess.run(["/home/user/start_server.sh"], check=True)

    # Wait for server to bind to port 8080
    assert wait_for_port(8080), "Server did not bind to port 8080 within the timeout."

    base_url = "http://localhost:8080"

    def post_artifact(name, version, deps):
        data = json.dumps({"name": name, "version": version, "deps": deps}).encode("utf-8")
        req = urllib.request.Request(f"{base_url}/artifacts", data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def get_resolve(name, version):
        req = urllib.request.Request(f"{base_url}/resolve/{name}/{version}")
        try:
            with urllib.request.urlopen(req) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    # 1. Test Successful Artifact Uploads
    status, _ = post_artifact("base", "1.0", [])
    assert status == 201, f"Expected 201 for base artifact, got {status}"

    status, _ = post_artifact("mid", "1.0", ["base@1.0"])
    assert status == 201, f"Expected 201 for mid artifact, got {status}"

    status, _ = post_artifact("top", "1.0", ["mid@1.0"])
    assert status == 201, f"Expected 201 for top artifact, got {status}"

    # 2. Test Build Order Resolution
    status, data = get_resolve("top", "1.0")
    assert status == 200, f"Expected 200 for resolve, got {status}"
    assert "build_order" in data, "Response missing 'build_order' key"
    expected_order = ["base@1.0", "mid@1.0", "top@1.0"]
    assert data["build_order"] == expected_order, f"Expected build order {expected_order}, got {data['build_order']}"

    # 3. Test Cycle Detection
    status, _ = post_artifact("cycleA", "1.0", ["cycleB@1.0"])
    assert status == 201, f"Expected 201 for cycleA artifact, got {status}"

    status, _ = post_artifact("cycleB", "1.0", ["cycleA@1.0"])
    assert status == 400, f"Expected 400 for cyclic dependency, got {status}"

    # 4. Test Rate Limiting
    # 5 requests already made. Limit is 10 per minute.
    # Make up to 10 more requests; at least one should be 429.
    rate_limited = False
    for i in range(10):
        status, _ = post_artifact(f"spam{i}", "1.0", [])
        if status == 429:
            rate_limited = True
            break

    assert rate_limited, "Rate limiting (429) was not triggered after exceeding 10 requests per minute."