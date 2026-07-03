# test_final_state.py
import socket
import json
import pytest

def send_request_and_get_response(request_str):
    host = '127.0.0.1'
    port = 9090
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((host, port))
            s.sendall(request_str.encode('utf-8'))

            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
                if b'\n' in chunk:
                    break
            return response.decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with the server at {host}:{port}: {e}")

def test_server_response_A_2():
    req = '{"start_node": "A", "max_hops": 2}\n'
    resp = send_request_and_get_response(req)

    assert resp.strip() != "", "Received empty response from server."

    try:
        parsed_resp = json.loads(resp)
    except json.JSONDecodeError as e:
        pytest.fail(f"Response is not valid JSON: {resp.strip()} (Error: {e})")

    assert isinstance(parsed_resp, list), f"Expected a JSON array, got {type(parsed_resp)}"
    assert set(parsed_resp) == {"B", "C", "D", "X"}, f"Expected nodes {{'B', 'C', 'D', 'X'}}, got {set(parsed_resp)}"

def test_server_response_B_1():
    req = '{"start_node": "B", "max_hops": 1}\n'
    resp = send_request_and_get_response(req)

    assert resp.strip() != "", "Received empty response from server."

    try:
        parsed_resp = json.loads(resp)
    except json.JSONDecodeError as e:
        pytest.fail(f"Response is not valid JSON: {resp.strip()} (Error: {e})")

    assert isinstance(parsed_resp, list), f"Expected a JSON array, got {type(parsed_resp)}"
    assert set(parsed_resp) == {"C"}, f"Expected nodes {{'C'}}, got {set(parsed_resp)}"