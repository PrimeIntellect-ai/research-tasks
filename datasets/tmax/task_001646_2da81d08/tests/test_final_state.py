# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_patch_order_file():
    patch_order_path = "/home/user/patch_order.txt"
    assert os.path.isfile(patch_order_path), f"Patch order log is missing: {patch_order_path}"

    with open(patch_order_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_order = [
        "base_init.patch",
        "core_utils.patch",
        "math_routines.patch",
        "analytics_engine.patch"
    ]

    assert lines == expected_order, f"Patch order is incorrect. Expected {expected_order}, got {lines}"

def test_cpp_binary_valgrind():
    binary_path = "/home/user/legacy_lib/analytics_engine"
    assert os.path.isfile(binary_path), f"Compiled binary missing: {binary_path}"

    # Run valgrind to check for memory leaks and errors
    result = subprocess.run(
        ["valgrind", "--error-exitcode=1", "--leak-check=full", binary_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Valgrind failed. The C++ binary has memory issues or crashed.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_rust_service_graph():
    url = "http://127.0.0.1:8080/graph"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Rust service at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for GET /graph, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /graph is not valid JSON: {response.text}")

    expected_order = [
        "base_init.patch",
        "core_utils.patch",
        "math_routines.patch",
        "analytics_engine.patch"
    ]

    assert data == expected_order, f"Expected /graph to return {expected_order}, got {data}"

def test_rust_service_verify_unauthorized():
    url = "http://127.0.0.1:8080/verify"
    try:
        response = requests.post(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Rust service at {url}: {e}")

    assert response.status_code in [401, 403], f"Expected 401 or 403 for POST /verify without auth, got {response.status_code}"

def test_rust_service_verify_authorized():
    url = "http://127.0.0.1:8080/verify"
    headers = {"Authorization": "Bearer artifact-token-992"}
    try:
        response = requests.post(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Rust service at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for POST /verify with auth, got {response.status_code}. Response: {response.text}"

    expected_text = "Analytics Engine V2: 0 memory leaks. Execution successful."
    assert expected_text in response.text, f"Expected '{expected_text}' in response body, got '{response.text}'"