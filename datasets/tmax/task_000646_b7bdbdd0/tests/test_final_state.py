# test_final_state.py

import socket
import pytest

def send_and_receive(payload: str, timeout=5.0) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect(('127.0.0.1', 8888))
            s.sendall(payload.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except ConnectionRefusedError:
        pytest.fail("Connection refused. Make sure the C server is running and listening on 127.0.0.1:8888.")
    except socket.timeout:
        pytest.fail("Socket timed out. The server accepted the connection but didn't respond in time.")
    except Exception as e:
        pytest.fail(f"Unexpected socket error: {e}")

def test_server_response_basic():
    payload = '{"ts": "2023-01-01T00:00:00Z", "msg": "Test\\u0021"}\n'
    response = send_and_receive(payload)

    response = response.strip()
    if "999" in response:
        pytest.fail(f"Server returned anomaly score 999 indicating unescaped unicode '\\' was sent to the analyzer. Response: {response}")

    expected = "1672531200,49"
    assert response == expected, f"Expected '{expected}', got '{response}'"

def test_server_response_complex():
    payload = '{"ts": "2023-11-15T08:30:00Z", "msg": "High CPU load on db-node-01\\u002e"}\n'
    response = send_and_receive(payload)

    response = response.strip()
    if "999" in response:
        pytest.fail(f"Server returned anomaly score 999 indicating unescaped unicode '\\' was sent to the analyzer. Response: {response}")

    expected = "1700037000,85"
    assert response == expected, f"Expected '{expected}', got '{response}'"