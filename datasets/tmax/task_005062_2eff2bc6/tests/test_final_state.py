# test_final_state.py

import os
import json
import pytest

def test_makefile_exists():
    path = "/home/user/Makefile"
    assert os.path.isfile(path), f"Makefile does not exist at {path}"
    with open(path, "r") as f:
        content = f.read()
    for target in ["build", "run", "bench", "all"]:
        assert target in content, f"Makefile is missing target: {target}"

def test_python_scripts_exist():
    for script in ["parse_routes.py", "rate_limit.py"]:
        path = f"/home/user/{script}"
        assert os.path.isfile(path), f"Python script {script} does not exist at {path}"

def test_libfilter_so_exists():
    path = "/home/user/libfilter.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist"

def test_routes_json():
    path = "/home/user/routes.json"
    assert os.path.isfile(path), f"JSON output {path} does not exist"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON")

    expected = [
        {"path": "/api/login", "method": "POST", "limit": 2},
        {"path": "/api/data", "method": "GET", "limit": 4}
    ]

    assert isinstance(data, list), f"{path} must contain a JSON array"

    # Sort both lists by path to ensure order doesn't fail the test if they used a dict internally
    data_sorted = sorted(data, key=lambda x: x.get("path", ""))
    expected_sorted = sorted(expected, key=lambda x: x["path"])

    assert data_sorted == expected_sorted, f"Parsed JSON data in {path} does not match expected output"

def test_banned_ips():
    path = "/home/user/banned_ips.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["10.0.0.5", "192.168.1.100"]
    assert lines == expected, f"Banned IPs in {path} do not match expected output"

def test_benchmark_log():
    path = "/home/user/benchmark.log"
    assert os.path.isfile(path), f"Benchmark log {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    # Check for common outputs of /usr/bin/time -v
    assert "User time" in content or "Maximum resident set size" in content or "Elapsed (wall clock) time" in content, \
        f"{path} does not appear to contain the output of /usr/bin/time -v"