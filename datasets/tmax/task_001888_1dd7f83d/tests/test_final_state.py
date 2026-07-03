# test_final_state.py

import os
import socket
import pytest
import subprocess

def test_rate_limit_extracted():
    txt_path = "/app/rate_limit.txt"
    assert os.path.isfile(txt_path), f"Expected file not found: {txt_path}"
    with open(txt_path, "r") as f:
        content = f.read().strip()
    assert content == "5", f"Expected rate limit to be '5', but got '{content}'"

def test_server_compiled():
    server_binary = "/app/workspace/server"
    assert os.path.isfile(server_binary), "Server binary not found. The project did not compile successfully."
    assert os.access(server_binary, os.X_OK), "Server binary is not executable."

def test_server_listening():
    # Check if port 50051 is listening
    port_open = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        result = s.connect_ex(('127.0.0.1', 50051))
        if result == 0:
            port_open = True
    assert port_open, "Expected server to be listening on port 50051, but it is not."

def test_extern_c_added():
    header_path = "/app/workspace/numalgo.h"
    assert os.path.isfile(header_path), f"Expected header file not found: {header_path}"
    with open(header_path, "r") as f:
        content = f.read()
    assert 'extern "C"' in content, "Expected 'extern \"C\"' block to be added to numalgo.h to fix the linking issue."