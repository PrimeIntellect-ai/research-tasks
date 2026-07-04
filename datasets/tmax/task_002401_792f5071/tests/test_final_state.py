# test_final_state.py
import os
import socket
import pytest

def test_files_exist():
    assert os.path.isfile("/home/user/ids_sink.c"), "/home/user/ids_sink.c does not exist"
    assert os.path.isfile("/home/user/ids_sink"), "/home/user/ids_sink executable does not exist"
    assert os.access("/home/user/ids_sink", os.X_OK), "/home/user/ids_sink is not executable"

def send_tcp_request(host, port, payload):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((host, port))
            s.sendall(payload)
            response = s.recv(1024)
            return response.decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with {host}:{port}: {e}")

def test_ids_sink_malicious_redirect():
    payload = b"GET /login?redirect=http://evil.com/?token=SEC-99887766\r\n"
    expected_response = "ALERT: MALICIOUS REDIRECT DETECTED\n"
    response = send_tcp_request("127.0.0.1", 8080, payload)
    assert response == expected_response, f"Expected '{expected_response}', but got '{response}'"

def test_ids_sink_normal_redirect():
    payload = b"GET /login?redirect=/dashboard\r\n"
    expected_response = "OK\n"
    response = send_tcp_request("127.0.0.1", 8080, payload)
    assert response == expected_response, f"Expected '{expected_response}', but got '{response}'"

def test_ids_sink_missing_redirect_path():
    payload = b"POST /api/data HTTP/1.1\r\nHost: example.com\r\n\r\ntoken=SEC-99887766"
    expected_response = "OK\n"
    response = send_tcp_request("127.0.0.1", 8080, payload)
    assert response == expected_response, f"Expected '{expected_response}', but got '{response}'"