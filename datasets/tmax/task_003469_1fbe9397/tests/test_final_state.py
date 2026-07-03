# test_final_state.py

import os
import requests
import pytest

def test_router_h_exists():
    """Verify that the router header file was generated."""
    assert os.path.exists("/home/user/router.h"), "Missing /home/user/router.h"

def test_server_binary_exists():
    """Verify that the C server was compiled and is executable."""
    assert os.path.exists("/home/user/server.c"), "Missing /home/user/server.c"
    assert os.path.exists("/home/user/server"), "Missing /home/user/server binary"
    assert os.access("/home/user/server", os.X_OK), "/home/user/server is not executable"

def test_server_exec_route_10():
    """Verify the execution route with init=10 returns the correct VM output."""
    try:
        response = requests.get("http://127.0.0.1:8080/api/exec?init=10", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text.strip() == "23", f"Expected response body '23', got '{response.text}'"

def test_server_exec_route_5():
    """Verify the execution route with init=5 returns the correct VM output."""
    try:
        response = requests.get("http://127.0.0.1:8080/api/exec?init=5", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    # init=5 -> INC(6) -> INC(7) -> MUL(14) -> DEC(13) -> RET(13)
    assert response.text.strip() == "13", f"Expected response body '13', got '{response.text}'"

def test_server_404_route():
    """Verify that an invalid route returns a 404 Not Found."""
    try:
        response = requests.get("http://127.0.0.1:8080/invalid", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at 127.0.0.1:8080: {e}")

    assert response.status_code == 404, f"Expected status code 404 for invalid route, got {response.status_code}"