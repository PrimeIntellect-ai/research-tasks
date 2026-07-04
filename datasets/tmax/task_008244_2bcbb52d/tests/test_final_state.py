# test_final_state.py
import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_makefile_compiles():
    reverser_bin = os.path.join(PROJECT_DIR, "reverser")
    if os.path.exists(reverser_bin):
        os.remove(reverser_bin)

    result = subprocess.run(["make"], cwd=PROJECT_DIR, capture_output=True)
    assert result.returncode == 0, f"Make failed with error: {result.stderr.decode()}"
    assert os.path.isfile(reverser_bin), "Makefile did not produce an executable named 'reverser'"
    assert os.access(reverser_bin, os.X_OK), "'reverser' binary is not executable"

def test_reverser_logic():
    reverser_bin = os.path.join(PROJECT_DIR, "reverser")
    assert os.path.isfile(reverser_bin), "reverser binary is missing, cannot test logic"

    result = subprocess.run([reverser_bin], input=b"hello", capture_output=True)
    assert result.stdout == b"olleh", f"Expected 'olleh', got {result.stdout!r}"

def test_prop_test_script():
    script_path = os.path.join(PROJECT_DIR, "prop_test.sh")
    log_path = os.path.join(PROJECT_DIR, "test_results.log")

    assert os.path.isfile(script_path), "prop_test.sh script is missing"
    assert os.access(script_path, os.X_OK), "prop_test.sh is not executable"

    if os.path.exists(log_path):
        os.remove(log_path)

    result = subprocess.run([script_path], cwd=PROJECT_DIR, capture_output=True)
    assert result.returncode == 0, f"prop_test.sh failed to execute: {result.stderr.decode()}"

    assert os.path.isfile(log_path), "test_results.log was not created by prop_test.sh"
    with open(log_path, "r") as f:
        content = f.read()
    assert "PROPERTY TEST PASSED" in content, "test_results.log does not contain 'PROPERTY TEST PASSED'"

def test_benchmark_script():
    script_path = os.path.join(PROJECT_DIR, "benchmark.sh")
    log_path = os.path.join(PROJECT_DIR, "benchmark.log")
    payload_path = os.path.join(PROJECT_DIR, "payload.txt")

    assert os.path.isfile(script_path), "benchmark.sh script is missing"
    assert os.access(script_path, os.X_OK), "benchmark.sh is not executable"

    if os.path.exists(log_path):
        os.remove(log_path)
    if os.path.exists(payload_path):
        os.remove(payload_path)

    result = subprocess.run([script_path], cwd=PROJECT_DIR, capture_output=True)
    assert result.returncode == 0, f"benchmark.sh failed to execute: {result.stderr.decode()}"

    assert os.path.isfile(log_path), "benchmark.log was not created by benchmark.sh"
    with open(log_path, "r") as f:
        content = f.read()
    assert "BENCHMARK COMPLETED" in content, "benchmark.log does not contain 'BENCHMARK COMPLETED'"

    assert os.path.isfile(payload_path), "payload.txt was not created by benchmark.sh"
    payload_size = os.path.getsize(payload_path)
    assert payload_size == 50000, f"payload.txt size is {payload_size}, expected exactly 50000"

    with open(payload_path, "r") as f:
        payload_content = f.read()
    assert payload_content == "A" * 50000, "payload.txt does not contain exactly 50,000 'A' characters"