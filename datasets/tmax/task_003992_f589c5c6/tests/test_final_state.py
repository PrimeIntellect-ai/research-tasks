# test_final_state.py
import os
import socket
import json
import pytest

def test_libmathops_makefile_fixed():
    """Check that the Makefile in the vendored library has -fPIC."""
    with open("/app/libmathops-1.2.0/Makefile", "r") as f:
        content = f.read()
    assert "-fPIC" in content, "Makefile in /app/libmathops-1.2.0 is still missing -fPIC"

def test_fibfast_memory_leak_fixed():
    """Check that the memory leak in fibfast.c is fixed by calling free()."""
    with open("/app/pr-104/fibfast.c", "r") as f:
        content = f.read()
    assert "free(" in content, "fibfast.c is missing a call to free() to fix the memory leak"

def test_server_script_exists():
    """Check that the server script was created."""
    assert os.path.isfile("/home/user/server.sh"), "/home/user/server.sh does not exist"

def test_server_response():
    """Check that the server responds correctly to a single request."""
    req = {"n": 10, "mod": 100}
    req_str = json.dumps(req) + "\n"

    try:
        with socket.create_connection(("127.0.0.1", 9090), timeout=5) as sock:
            sock.sendall(req_str.encode("utf-8"))

            # Read until newline
            response_data = b""
            while b"\n" not in response_data:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                response_data += chunk

        assert response_data, "Server closed connection without responding"
        resp_str = response_data.decode("utf-8").strip()
        resp = json.loads(resp_str)

        assert "result" in resp, f"Response missing 'result' key: {resp}"
        assert resp["result"] == 55, f"Expected result 55, got {resp['result']}"

    except ConnectionRefusedError:
        pytest.fail("Server is not listening on 127.0.0.1:9090")
    except socket.timeout:
        pytest.fail("Server timed out while responding")
    except json.JSONDecodeError:
        pytest.fail(f"Server returned invalid JSON: {response_data}")

def test_server_burst_requests():
    """Check that the server can handle a burst of requests without crashing."""
    req = {"n": 100, "mod": 1000000007}
    req_str = json.dumps(req) + "\n"

    # Send a burst of requests
    for _ in range(100):
        try:
            with socket.create_connection(("127.0.0.1", 9090), timeout=5) as sock:
                sock.sendall(req_str.encode("utf-8"))

                response_data = b""
                while b"\n" not in response_data:
                    chunk = sock.recv(1024)
                    if not chunk:
                        break
                    response_data += chunk

            assert response_data, "Server closed connection without responding during burst"
            resp_str = response_data.decode("utf-8").strip()
            resp = json.loads(resp_str)
            assert resp.get("result") == 687995182, f"Unexpected result during burst: {resp}"
        except Exception as e:
            pytest.fail(f"Server failed during burst requests: {e}")