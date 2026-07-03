# test_final_state.py
import pytest
import requests
import time
import socket

def wait_for_port(port, host='127.0.0.1', timeout=5.0):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.1)
    return False

@pytest.fixture(scope="module")
def server_url():
    assert wait_for_port(9000), "Server is not listening on port 9000"
    return "http://127.0.0.1:9000/process"

def test_process_normal_csv(server_url):
    csv_data = (
        "timestamp,sensor1,sensor2,sensor3\n"
        "2023-01-01T00:00:00Z,10.0,60.0,20.0\n"
        "2023-01-01T00:01:00Z,80.0,10.0,90.0\n"
    )
    expected_output = (
        "ALARM: Sensor sensor2 at 2023-01-01T00:00:00Z triggered an anomaly!\n"
        "ALARM: Sensor sensor1 at 2023-01-01T00:01:00Z triggered an anomaly!\n"
        "ALARM: Sensor sensor3 at 2023-01-01T00:01:00Z triggered an anomaly!\n"
    )

    response = requests.post(server_url, data=csv_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "text/plain" in response.headers.get("Content-Type", ""), "Expected Content-Type: text/plain"
    assert response.text == expected_output, f"Output mismatch.\nExpected:\n{expected_output}\nGot:\n{response.text}"

def test_process_csv_with_embedded_newlines(server_url):
    csv_data = (
        "timestamp,sensor1,sensor2,sensor3\n"
        "2023-01-01T00:02:00Z,10.0,\"60.0\nnew\",20.0\n"
        "2023-01-01T00:03:00Z,80.0,10.0,90.0\n"
        "2023-01-01T00:04:00Z,90.0,\"40.0\",10.0\n"
    )
    expected_output = (
        "ALARM: Sensor sensor1 at 2023-01-01T00:03:00Z triggered an anomaly!\n"
        "ALARM: Sensor sensor3 at 2023-01-01T00:03:00Z triggered an anomaly!\n"
        "ALARM: Sensor sensor1 at 2023-01-01T00:04:00Z triggered an anomaly!\n"
    )

    response = requests.post(server_url, data=csv_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.text == expected_output, f"Output mismatch for embedded newlines.\nExpected:\n{expected_output}\nGot:\n{response.text}"