# test_final_state.py

import os
import socket
import pytest

def test_lua_makefile_fixed():
    makefile_path = "/app/vendored/lua-5.4.6/src/Makefile"
    assert os.path.isfile(makefile_path), f"Lua Makefile {makefile_path} is missing"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-lbrokenmath" not in content, "Makefile still contains the broken flag '-lbrokenmath'"
    assert "-lm" in content, "Makefile does not contain the required math library flag '-lm'"

def test_liblua_built():
    liblua_path = "/app/vendored/lua-5.4.6/src/liblua.a"
    assert os.path.isfile(liblua_path), f"Lua static library {liblua_path} was not built"

def test_workspace_files_exist():
    workspace = "/home/user/workspace"
    assert os.path.isfile(os.path.join(workspace, "server.cpp")), "server.cpp is missing"
    assert os.path.isfile(os.path.join(workspace, "Makefile")), "Makefile in workspace is missing"
    assert os.path.isfile(os.path.join(workspace, "lua_server")), "lua_server executable is missing"

def send_and_receive(host, port, message):
    with socket.create_connection((host, port), timeout=5) as sock:
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
    return response.strip()

def test_tcp_server_interaction():
    host = "127.0.0.1"
    port = 8888

    # First interaction
    try:
        response1 = send_and_receive(host, port, "return 17 * 3\n")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with the server for the first request: {e}")

    assert response1 in ["51", "51.0"], f"Expected 51 or 51.0, but got: {response1}"

    # Second interaction
    try:
        response2 = send_and_receive(host, port, "return math.sqrt(144)\n")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with the server for the second request: {e}")

    assert response2 in ["12", "12.0"], f"Expected 12 or 12.0, but got: {response2}"