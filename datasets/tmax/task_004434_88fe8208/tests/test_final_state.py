# test_final_state.py

import os
import struct
import socket
import pickle
import json
import requests
import pytest

def test_http_proxy_status_and_headers():
    """
    Test the HTTP proxy on port 8080.
    It should forward the request to the Go backend and inject the X-Migrated-By header.
    """
    try:
        # We send a request to the proxy
        response = requests.get("http://127.0.0.1:8080/status", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP proxy on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected 200 OK from proxy, got {response.status_code}"

    # Send a POST to any route to check if headers are echoed back, or just rely on the proxy functioning
    try:
        post_resp = requests.post("http://127.0.0.1:8080/test_header", json={"test": "data"}, timeout=5)
        if post_resp.status_code == 200:
            data = post_resp.json()
            # The Go backend echoes the JSON payload back with {"status": "ok", "echo": <data>}
            assert data.get("status") == "ok", "Expected status 'ok' in backend response"
            assert data.get("echo") == {"test": "data"}, "Expected echoed data to match"
    except Exception as e:
        pytest.fail(f"Proxy POST request failed: {e}")


def test_tcp_translator():
    """
    Test the TCP translator on port 9090.
    It should accept a length-prefixed pickled dict, forward it as JSON to the Go backend,
    and return a length-prefixed pickled response.
    """
    payload_dict = {"route": "/test_tcp", "data": {"key": "value"}}
    try:
        # Use protocol 2 to simulate Python 2 client
        payload = pickle.dumps(payload_dict, protocol=2)
    except Exception as e:
        pytest.fail(f"Failed to pickle payload: {e}")

    msg = struct.pack(">I", len(payload)) + payload

    try:
        s = socket.create_connection(("127.0.0.1", 9090), timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to connect to TCP proxy on 127.0.0.1:9090: {e}")

    try:
        s.sendall(msg)

        # Read 4-byte length prefix
        length_data = b""
        while len(length_data) < 4:
            chunk = s.recv(4 - len(length_data))
            if not chunk:
                break
            length_data += chunk

        assert len(length_data) == 4, "Failed to read 4-byte length prefix from TCP proxy"

        response_length = struct.unpack(">I", length_data)[0]

        # Read the response payload
        response_payload = b""
        while len(response_payload) < response_length:
            chunk = s.recv(response_length - len(response_payload))
            if not chunk:
                break
            response_payload += chunk

        assert len(response_payload) == response_length, "Failed to read complete response payload"

        # Unpickle the response
        try:
            response_dict = pickle.loads(response_payload)
        except Exception as e:
            pytest.fail(f"Failed to unpickle response from TCP proxy: {e}")

        assert isinstance(response_dict, dict), "Expected unpickled response to be a dictionary"
        assert response_dict.get("status") == "ok", f"Expected status 'ok', got {response_dict.get('status')}"
        assert response_dict.get("echo") == {"key": "value"}, f"Expected echo {{'key': 'value'}}, got {response_dict.get('echo')}"

    finally:
        s.close()