# test_final_state.py
import pytest
import requests
import subprocess
import json
import hashlib
import os

def redis_set(key, value):
    try:
        subprocess.run(["redis-cli", "SET", key, value], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to set Redis key {key}: {e.stderr.decode()}")

def test_api_resolution():
    # Populate Redis with a valid DAG
    # root_app:1.0 -> libB:2.0, libC:3.0
    # libB:2.0 -> libD:1.5
    # libC:3.0 -> libD:1.5
    # libD:1.5 -> []
    redis_set("artifact:root_app:1.0:deps", json.dumps([{"name": "libB", "version": "2.0"}, {"name": "libC", "version": "3.0"}]))
    redis_set("artifact:root_app:1.0:checksum", "aaaa")

    redis_set("artifact:libB:2.0:deps", json.dumps([{"name": "libD", "version": "1.5"}]))
    redis_set("artifact:libB:2.0:checksum", "bbbb")

    redis_set("artifact:libC:3.0:deps", json.dumps([{"name": "libD", "version": "1.5"}]))
    redis_set("artifact:libC:3.0:checksum", "cccc")

    redis_set("artifact:libD:1.5:deps", json.dumps([]))
    redis_set("artifact:libD:1.5:checksum", "dddd")

    try:
        resp = requests.get("http://127.0.0.1:8080/api/v1/artifacts/resolve/root_app?version=1.0", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Python API: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("artifact") == "root_app", "Response artifact name mismatch"
    assert data.get("version") == "1.0", "Response artifact version mismatch"

    deps = data.get("resolved_dependencies", [])
    names = [d.get("name") for d in deps]

    assert "libD" in names, "libD missing from resolved dependencies"
    assert "libB" in names, "libB missing from resolved dependencies"
    assert "libC" in names, "libC missing from resolved dependencies"
    assert "root_app" not in names, "root_app should not be in its own dependencies list"

    idx_d = names.index("libD")
    idx_b = names.index("libB")
    idx_c = names.index("libC")

    assert idx_d < idx_b, "Topological sort failed: libD must appear before libB"
    assert idx_d < idx_c, "Topological sort failed: libD must appear before libC"

    # Check aggregated checksum based on the actual valid topological sort returned
    if idx_b < idx_c:
        concat_str = "dddd" + "bbbb" + "cccc" + "aaaa"
    else:
        concat_str = "dddd" + "cccc" + "bbbb" + "aaaa"

    expected_checksum = hashlib.sha256(concat_str.encode('utf-8')).hexdigest()
    assert data.get("aggregated_checksum") == expected_checksum, "Aggregated checksum is incorrect"

def test_api_circular_dependency():
    redis_set("artifact:circA:1:deps", json.dumps([{"name": "circB", "version": "1"}]))
    redis_set("artifact:circA:1:checksum", "1111")
    redis_set("artifact:circB:1:deps", json.dumps([{"name": "circA", "version": "1"}]))
    redis_set("artifact:circB:1:checksum", "2222")

    try:
        resp = requests.get("http://127.0.0.1:8080/api/v1/artifacts/resolve/circA?version=1", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Python API: {e}")

    assert resp.status_code == 400, f"Expected HTTP 400 for circular dependency, got {resp.status_code}"

    try:
        data = resp.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "error" in data, "Expected 'error' key in response for circular dependency"
    assert "circular dependency detected" in data["error"].lower(), "Expected error message to mention circular dependency"

def test_property_based_tests_exist_and_pass():
    test_file = "/home/user/tests/test_graph.py"
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist"

    with open(test_file, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "The test file does not seem to import or use 'hypothesis'"
    assert "@given" in content, "The test file does not seem to use the '@given' decorator from hypothesis"

    res = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    assert res.returncode == 0, f"pytest on {test_file} failed:\n{res.stdout}\n{res.stderr}"