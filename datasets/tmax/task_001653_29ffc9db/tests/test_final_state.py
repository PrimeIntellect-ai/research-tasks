# test_final_state.py
import os
import re
import pytest

def test_cmakelists_updated():
    cmake_path = "/home/user/emulator_port/CMakeLists.txt"
    assert os.path.isfile(cmake_path), f"File not found: {cmake_path}"

    with open(cmake_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for C++17
    has_cxx17 = re.search(r"cxx_std_17|CMAKE_CXX_STANDARD\s+17", content, re.IGNORECASE)
    assert has_cxx17, "CMakeLists.txt does not enforce C++17 standard."

    # Check for Threads
    has_threads = re.search(r"Threads::Threads", content) or re.search(r"-pthread", content)
    assert has_threads, "CMakeLists.txt does not link the Threads package."

def test_ci_workflow_exists():
    workflow_path = "/home/user/emulator_port/.github/workflows/ci.yml"
    assert os.path.isfile(workflow_path), f"CI workflow file not found at {workflow_path}"

    with open(workflow_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "ubuntu-latest" in content, "CI workflow does not use 'ubuntu-latest' runner."
    assert "cmake" in content.lower(), "CI workflow does not appear to configure/build CMake."

def test_benchmark_log_passed():
    log_path = "/home/user/emulator_port/benchmark_metrics.log"
    assert os.path.isfile(log_path), f"Benchmark log not found: {log_path}"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "BENCHMARK_COMPLETE: ALL PASS" in content, "Benchmark log does not indicate all tests passed. Ensure the server correctly handles both valid and invalid requests."

def test_bf_server_built():
    # It could be built in the source directory or a build directory.
    # We check if an executable named bf_server exists anywhere in the project.
    project_dir = "/home/user/emulator_port"
    found = False
    for root, dirs, files in os.walk(project_dir):
        if "bf_server" in files:
            filepath = os.path.join(root, "bf_server")
            if os.access(filepath, os.X_OK):
                found = True
                break

    assert found, "The 'bf_server' executable was not found. Ensure the project builds successfully."