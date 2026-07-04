# test_final_state.py

import os
import stat
import requests
import pytest
import time

def test_makefile_fixed():
    makefile_path = '/app/extractor/Makefile'
    assert os.path.isfile(makefile_path), f"The file {makefile_path} is missing."
    with open(makefile_path, 'r') as f:
        content = f.read()
    assert "-lm" in content, "The Makefile does not contain the '-lm' flag required for linking math functions."

def test_extractor_compiled():
    binary_path = '/app/extractor/extractor'
    assert os.path.isfile(binary_path), f"The binary {binary_path} was not compiled."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_commands_extracted():
    commands_path = '/home/user/commands.txt'
    assert os.path.isfile(commands_path), f"The file {commands_path} is missing."
    with open(commands_path, 'r') as f:
        content = f.read()
    assert "LOAD 100" in content, "The extracted commands do not seem correct."

def test_interpreter_exists():
    interpreter_path = '/home/user/interpreter.sh'
    assert os.path.isfile(interpreter_path), f"The file {interpreter_path} is missing."

def test_server_script_exists():
    server_path = '/home/user/server.sh'
    assert os.path.isfile(server_path), f"The file {server_path} is missing."

def test_http_service_responses():
    url = "http://127.0.0.1:9090/state"
    expected_result = {"accumulator": 84}

    for i in range(3):
        try:
            response = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request {i+1} failed: {e}. Is the server running and handling multiple requests?")

        assert response.status_code == 200, f"Request {i+1} failed: Expected status 200, got {response.status_code}"
        assert "application/json" in response.headers.get("Content-Type", ""), f"Request {i+1} failed: Expected Content-Type application/json"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Request {i+1} failed: Response is not valid JSON: {response.text}")

        assert data == expected_result, f"Request {i+1} failed: Expected {expected_result}, got {data}"
        time.sleep(0.1)