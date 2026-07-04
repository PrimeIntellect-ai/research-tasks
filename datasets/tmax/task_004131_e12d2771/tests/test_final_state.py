# test_final_state.py
import socket
import pytest

def get_expected(x):
    return (x * x + x + 41) % 1000

def test_tcp_service_responses():
    host = '127.0.0.1'
    port = 9999

    # Test normal inputs and crash-triggering inputs (multiples of 7)
    test_cases = [1, 2, 5, 7, 10, 14, 21, 100]

    for x in test_cases:
        expected = get_expected(x)
        try:
            with socket.create_connection((host, port), timeout=3) as s:
                s.sendall(f"{x}\n".encode('utf-8'))
                response = s.recv(1024).decode('utf-8').strip()
                assert response == str(expected), f"For input {x}, expected {expected} but got {response}"
        except ConnectionRefusedError:
            pytest.fail(f"Connection refused on {host}:{port}. Ensure the TCP service is running.")
        except socket.timeout:
            pytest.fail(f"Timeout waiting for response from {host}:{port} for input {x}.")
        except Exception as e:
            pytest.fail(f"Unexpected error when testing input {x}: {e}")