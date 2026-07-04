# test_final_state.py

import os
import json
import glob
import subprocess
import urllib.request
import time

def test_result_json():
    result_path = "/home/user/result.json"
    assert os.path.exists(result_path), f"File {result_path} does not exist."

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{result_path} does not contain valid JSON."

    assert "result" in data, f"{result_path} JSON does not contain the 'result' key."
    assert data["result"] == 50, f"Expected result to be 50, but got {data['result']}."

def test_nginx_running_and_proxying():
    # Check if we can hit Nginx on port 8080 and get the expected response
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/process")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 from Nginx, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            assert data.get("result") == 50, "Nginx proxy did not return the expected result."
    except Exception as e:
        assert False, f"Failed to connect to Nginx on port 8080 or proxy failed: {e}"

def test_app_py_running():
    # Check if we can hit app.py directly on port 9000
    try:
        req = urllib.request.Request("http://127.0.0.1:9000/process")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 from app.py, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            assert data.get("result") == 50, "app.py did not return the expected result."
    except Exception as e:
        assert False, f"Failed to connect to app.py on port 9000: {e}"

def test_extension_linked_correctly():
    # Find the compiled pyprocessor extension
    so_files = glob.glob("/home/user/app/pyprocessor*.so")
    assert so_files, "Could not find compiled pyprocessor extension (pyprocessor*.so) in /home/user/app/"

    so_file = so_files[0]

    # Run ldd to check linkage
    try:
        result = subprocess.run(["ldd", so_file], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        assert False, f"ldd failed on {so_file}: {e.stderr}"

    output = result.stdout

    # Check if libprocessor.so is resolved correctly
    expected_path = "/home/user/app/lib/libprocessor.so"
    found = False
    for line in output.splitlines():
        if "libprocessor.so" in line and expected_path in line:
            found = True
            break

    assert found, f"libprocessor.so is not correctly linked to {expected_path} in {so_file}. ldd output:\n{output}"

def test_nginx_conf_exists():
    conf_path = "/home/user/app/nginx.conf"
    assert os.path.exists(conf_path), f"Nginx configuration {conf_path} does not exist."
    assert os.path.isfile(conf_path), f"{conf_path} is not a file."