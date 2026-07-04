# test_final_state.py

import os
import subprocess
import json
import pytest

def test_libsmuggler_compiled():
    """Verify that libsmuggler.so is compiled and is a valid shared object."""
    so_path = '/home/user/smuggler/libsmuggler.so'
    assert os.path.isfile(so_path), f"Shared library {so_path} was not created."

    # Check if it's actually a shared object using the 'file' command
    result = subprocess.run(['file', so_path], capture_output=True, text=True)
    assert "shared object" in result.stdout, f"{so_path} is not compiled as a shared object. Check Makefile flags (-shared, -fPIC)."

def test_python_tests_pass():
    """Verify that the Python test suite passes without SMUGGLER_MODE pre-set in the environment."""
    # Run the tests with a clean environment (without SMUGGLER_MODE)
    env = os.environ.copy()
    env.pop("SMUGGLER_MODE", None)

    result = subprocess.run(
        ['python3', '-m', 'unittest', 'discover', 'tests'],
        cwd='/home/user/smuggler',
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Python tests failed or import order is still broken.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_go_server_compiled():
    """Verify that the Go target server is compiled into an executable."""
    exe_path = '/home/user/target/server'
    assert os.path.isfile(exe_path), f"Go server executable {exe_path} was not created."
    assert os.access(exe_path, os.X_OK), f"Go server {exe_path} is not executable."

def test_benchmark_script_exists():
    """Verify that the benchmark script was created."""
    script_path = '/home/user/benchmark.py'
    assert os.path.isfile(script_path), f"Benchmark script {script_path} is missing."

def test_benchmark_json_output():
    """Verify that the benchmark JSON output meets the requirements."""
    json_path = '/home/user/benchmark.json'
    assert os.path.isfile(json_path), f"Benchmark output {json_path} is missing."

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{json_path} does not contain valid JSON.")

    assert "status" in data, "Key 'status' missing in benchmark.json"
    assert data["status"] == "success", f"Expected status 'success', got {data['status']}"

    assert "duration" in data, "Key 'duration' missing in benchmark.json"
    assert isinstance(data["duration"], float), "Duration must be a float"
    assert data["duration"] >= 2.9, f"Benchmark duration {data['duration']} is less than the required 3 seconds (allowing slight float margin)."

    assert "requests_sent" in data, "Key 'requests_sent' missing in benchmark.json"
    assert isinstance(data["requests_sent"], int), "requests_sent must be an integer"
    assert data["requests_sent"] > 0, "requests_sent must be greater than 0"