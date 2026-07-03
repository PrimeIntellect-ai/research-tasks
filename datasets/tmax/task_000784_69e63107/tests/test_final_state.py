# test_final_state.py

import os
import socket
import pytest

def send_command(host: str, port: int, cmd: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((host, port))
        s.sendall(cmd.encode('utf-8'))

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
            if b'\n' in chunk:
                break
        return response.decode('utf-8')

def test_source_and_binary_exist():
    assert os.path.exists("/home/user/topology_server.cpp"), "C++ source file /home/user/topology_server.cpp is missing"
    assert os.path.exists("/home/user/topology_server"), "Compiled binary /home/user/topology_server is missing"
    assert os.access("/home/user/topology_server", os.X_OK), "Binary /home/user/topology_server is not executable"

def test_tcp_server_path_db1_db5():
    try:
        resp = send_command("127.0.0.1", 8080, "PATH db1 db5\n")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with server on 127.0.0.1:8080: {e}")

    assert resp == "db1,db2,db5 35\n", f"Expected 'db1,db2,db5 35\\n', got {repr(resp)}"

def test_tcp_server_path_db3_db2():
    try:
        resp = send_command("127.0.0.1", 8080, "PATH db3 db2\n")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with server on 127.0.0.1:8080: {e}")

    assert resp == "db3,db1,db2 25\n", f"Expected 'db3,db1,db2 25\\n', got {repr(resp)}"

def test_tcp_server_degree_db4():
    try:
        resp = send_command("127.0.0.1", 8080, "DEGREE db4\n")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with server on 127.0.0.1:8080: {e}")

    assert resp == "3\n", f"Expected '3\\n', got {repr(resp)}"

def test_tcp_server_degree_db1():
    try:
        resp = send_command("127.0.0.1", 8080, "DEGREE db1\n")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with server on 127.0.0.1:8080: {e}")

    assert resp == "2\n", f"Expected '2\\n', got {repr(resp)}"