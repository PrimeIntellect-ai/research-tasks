# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/release_prep"
SERVER_SECURE = os.path.join(BASE_DIR, "server_secure")
DEP_GRAPH = os.path.join(BASE_DIR, "dep_graph.txt")

def test_server_secure_exists_and_executable():
    assert os.path.isfile(SERVER_SECURE), f"File {SERVER_SECURE} does not exist. Did you run make?"
    assert os.access(SERVER_SECURE, os.X_OK), f"File {SERVER_SECURE} is not executable."

def test_symbols_in_executable():
    # Run nm to list symbols
    try:
        result = subprocess.run(["nm", SERVER_SECURE], capture_output=True, text=True, check=True)
        nm_output = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run nm on {SERVER_SECURE}: {e.stderr}")

    # init_telemetry_v2 must exist
    assert "init_telemetry_v2" in nm_output, "Symbol 'init_telemetry_v2' is missing from the executable. The stub was not linked correctly."

    # malicious_hook must NOT exist
    assert "malicious_hook" not in nm_output, "Symbol 'malicious_hook' was found in the executable. The malicious code was not removed."

def test_dep_graph():
    assert os.path.isfile(DEP_GRAPH), f"File {DEP_GRAPH} does not exist."

    with open(DEP_GRAPH, "r") as f:
        content = f.read().strip()

    # Parse the comma-separated list
    files = [f.strip() for f in content.split(",") if f.strip()]

    expected_files = {"server.o", "http_parser.o", "vendor/auth.o", "clean_stub.o"}
    actual_files = set(files)

    assert actual_files == expected_files, f"Expected dependency graph to contain exactly {expected_files}, but got {actual_files}."
    assert "malicious.o" not in actual_files, "malicious.o should not be in the dependency graph."