# test_final_state.py
import socket
import requests
import pytest

def test_http_status_port_9000():
    url = "http://127.0.0.1:9000/status"
    headers = {"Authorization": "Bearer sec_r3t_v1d30_t0k3n"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. The service may not be running correctly or the auth token is wrong."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to port 9000 failed: {e}. Is the service running and bound to 127.0.0.1:9000?")

def test_tcp_analysis_port_9001():
    host = "127.0.0.1"
    port = 9001
    command = b"ANALYZE /app/evidence.mp4\n"

    try:
        with socket.create_connection((host, port), timeout=15) as s:
            s.sendall(command)
            data = s.recv(1024).decode('utf-8')
            assert data.strip() == "FRAMES:142,143,144", f"Expected 'FRAMES:142,143,144', got '{data.strip()}'. The analyzer logic might be incorrect or incomplete."
    except socket.timeout:
        pytest.fail("TCP request to port 9001 timed out. The performance issue might not be fixed, or the service is hanging on corrupted frames.")
    except ConnectionRefusedError:
        pytest.fail("Connection refused on port 9001. Is the service running and bound to 127.0.0.1:9001?")
    except Exception as e:
        pytest.fail(f"TCP request to port 9001 failed: {e}")