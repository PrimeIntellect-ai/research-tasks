# test_final_state.py

import os
import socket
import pytest

def test_makefile_fixed():
    makefile_path = "/app/math_server/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} does not exist"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "math_utils.o" in content.split("server:")[1].split("\n")[1], "Makefile still has linker error"

def test_math_utils_fixed():
    math_utils_path = "/app/math_server/math_utils.cpp"
    assert os.path.isfile(math_utils_path), f"{math_utils_path} does not exist"
    with open(math_utils_path, "r") as f:
        content = f.read()
    assert "x = x - f(x) / df(x);" in content, "math_utils.cpp still has the mathematical regression"
    assert "x = x + f(x) / df(x);" not in content, "math_utils.cpp still has the mathematical regression"

def test_main_cpp_updated():
    main_path = "/app/math_server/main.cpp"
    assert os.path.isfile(main_path), f"{main_path} does not exist"
    with open(main_path, "r") as f:
        content = f.read()
    assert "8888" in content, "main.cpp does not have the updated port 8888"
    assert "1e-6" in content or "0.000001" in content, "main.cpp does not have the updated tolerance"

def test_server_running_and_correct():
    host = "127.0.0.1"
    port = 8888

    # Test with 3.0
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"3.0\n")
            response = s.recv(1024).decode("utf-8")
            assert response == "2.09455\n", f"Expected '2.09455\\n', got {repr(response)}"
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {host}:{port}. Is it running?")
    except socket.timeout:
        pytest.fail("Server connection timed out.")

    # Test with 0.0
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"0.0\n")
            response = s.recv(1024).decode("utf-8")
            assert response == "2.09455\n", f"Expected '2.09455\\n', got {repr(response)}"
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {host}:{port} for second test.")
    except socket.timeout:
        pytest.fail("Server connection timed out on second test.")