# test_final_state.py

import os
import subprocess
import ctypes
import time
import pytest

WORKSPACE_DIR = "/home/user/workspace"
BUILD_SCRIPT = os.path.join(WORKSPACE_DIR, "build.sh")
SERVER_FILE = os.path.join(WORKSPACE_DIR, "server.py")
CLIENT_FILE = os.path.join(WORKSPACE_DIR, "test_client.py")
C_FILE = os.path.join(WORKSPACE_DIR, "artifact_utils.c")
SO_FILE = os.path.join(WORKSPACE_DIR, "libartifact.so")
LOG_FILE = os.path.join(WORKSPACE_DIR, "test_result.log")

def test_build_script_exists_and_executable():
    assert os.path.isfile(BUILD_SCRIPT), f"Build script not found: {BUILD_SCRIPT}"
    assert os.access(BUILD_SCRIPT, os.X_OK), f"Build script is not executable: {BUILD_SCRIPT}"

def test_python_files_exist():
    assert os.path.isfile(SERVER_FILE), f"Server file not found: {SERVER_FILE}"
    assert os.path.isfile(CLIENT_FILE), f"Client file not found: {CLIENT_FILE}"

def test_build_and_c_logic():
    # Run the build script to ensure artifacts are generated
    result = subprocess.run([BUILD_SCRIPT], cwd=WORKSPACE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Build script failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    assert os.path.isfile(SO_FILE), f"Shared library not found after build: {SO_FILE}"

    # Load the library and test the C function directly to ensure the buffer overflow is fixed
    lib = ctypes.CDLL(SO_FILE)
    extract_version = lib.extract_version
    extract_version.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    extract_version.restype = None

    # Provide a 16-byte buffer (initialized to A's to detect overflow/null termination issues)
    buf = ctypes.create_string_buffer(b"A" * 20, 20)
    test_input = b"superlongversionstringthatwilloverflow_build123"

    extract_version(test_input, buf)

    # The output should be exactly 15 chars + null terminator
    extracted = buf.value
    assert extracted == b"superlongversio", f"Expected 'superlongversio', got {extracted}"

    # Check that the 16th byte is null
    assert buf[15] == b'\x00', "Buffer was not properly null-terminated at the 16th byte"
    # Check that bytes beyond 16 were not overwritten
    assert buf[16] == b'A', "Buffer overflow detected! Wrote past the 16-byte limit."

def test_grpc_server_and_client():
    # If the log file already exists and has the correct content, the agent ran it successfully
    if os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            content = f.read().strip()
        if "Extracted: superlongversio" in content:
            return # Success

    # Otherwise, we need to run the server and client to test them
    server_process = subprocess.Popen(
        ["python3", SERVER_FILE],
        cwd=WORKSPACE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Give the server a moment to start
        time.sleep(2)

        # Run the client
        client_result = subprocess.run(
            ["python3", CLIENT_FILE],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=10
        )
        assert client_result.returncode == 0, f"Client failed:\nSTDOUT: {client_result.stdout}\nSTDERR: {client_result.stderr}"

        # Check the log file again
        assert os.path.isfile(LOG_FILE), f"Log file not created: {LOG_FILE}"
        with open(LOG_FILE, "r") as f:
            content = f.read().strip()

        assert "Extracted: superlongversio" in content, f"Log file content incorrect. Got: {content}"

    finally:
        server_process.terminate()
        server_process.wait(timeout=5)