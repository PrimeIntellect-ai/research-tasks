# test_final_state.py

import socket
import time
import requests
import pytest

def test_iot_system_end_to_end():
    # UDP endpoint
    udp_ip = "127.0.0.1"
    udp_port = 5005

    # Payload (hex): 49 4f 54 00 05 00 00 00 00 00 00 00 18 fc ff ff
    # Magic: IOT\x00, Sensor: 5, Time: 0, Temp: -1000
    payload = bytes.fromhex("494f5400050000000000000018fcffff")

    # Send UDP packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(payload, (udp_ip, udp_port))
    except Exception as e:
        pytest.fail(f"Failed to send UDP packet to {udp_ip}:{udp_port}: {e}")
    finally:
        sock.close()

    # Give the system a moment to process the packet and forward it to the ingest API
    time.sleep(1.0)

    # HTTP endpoint
    http_url = "http://127.0.0.1:8081/latest?sensor_id=5"

    try:
        response = requests.get(http_url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to parser_service HTTP admin interface at {http_url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {http_url} is not valid JSON. Response body: {response.text}")

    assert "sensor_id" in data, f"Missing 'sensor_id' in response: {data}"
    assert "temperature" in data, f"Missing 'temperature' in response: {data}"

    assert data["sensor_id"] == 5, f"Expected sensor_id=5, got {data['sensor_id']}"
    assert data["temperature"] == -1000, f"Expected temperature=-1000, got {data['temperature']}. Ensure struct parsing uses signed integers for temperature and the token is correct."