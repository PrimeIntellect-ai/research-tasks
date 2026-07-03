# test_final_state.py

import os
import time
import requests
import pytest
import math

def test_makefile_patch_exists():
    patch_path = "/app/makefile.patch"
    assert os.path.isfile(patch_path), f"Patch file {patch_path} does not exist."
    with open(patch_path, "r") as f:
        content = f.read()
    assert "-lm" in content or "+lm" in content or "lm" in content, "The patch file does not seem to add the -lm flag."

def test_shared_library_compiled():
    so_path = "/app/tinymath/libtinymath.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not compiled."

def test_server_evaluate_endpoint():
    url = "http://127.0.0.1:8080/evaluate"

    # Wait briefly in case the server is slow to start, though it should be running
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get("http://127.0.0.1:8080/")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    payload1 = {"expression": "cos(0) * 5"}
    try:
        resp1 = requests.post(url, json=payload1, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server at 127.0.0.1:8080. Is it running?")

    assert resp1.status_code == 200, f"Expected status 200, got {resp1.status_code}. Response: {resp1.text}"
    data1 = resp1.json()
    assert "result" in data1, "Response JSON missing 'result' key."
    assert math.isclose(data1["result"], 5.0, abs_tol=1e-5), f"Expected result 5.0, got {data1['result']}"

    payload2 = {"expression": "sin(3.14159265359) + 42"}
    resp2 = requests.post(url, json=payload2, timeout=5)
    assert resp2.status_code == 200, f"Expected status 200, got {resp2.status_code}. Response: {resp2.text}"
    data2 = resp2.json()
    assert "result" in data2, "Response JSON missing 'result' key."
    assert math.isclose(data2["result"], 42.0, abs_tol=1e-5), f"Expected result ~42.0, got {data2['result']}"