# test_final_state.py
import socket
import time
import requests
import pytest

def test_pipeline_integration():
    # Send payloads to the TCP ingestor
    host = '127.0.0.1'
    port = 5000

    payloads = [
        b'{"message": "AABB"}\n',
        b'{"message": "corrupted...\n',
        b'\xff\xfe\x00\x00\n',
        b'{"message": "A"}\n'
    ]

    for payload in payloads:
        try:
            with socket.create_connection((host, port), timeout=2) as s:
                s.sendall(payload)
        except Exception as e:
            pytest.fail(f"Failed to connect and send data to TCP Ingestor at {host}:{port}: {e}")
        time.sleep(0.1)

    # Allow some time for Redis and the Processor to handle the messages
    time.sleep(1)

    # Query the HTTP processor
    url = 'http://127.0.0.1:8000/stats'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.fail(f"Failed to reach HTTP Processor at {url}: {e}")

    data = response.json()

    # Verify the stats
    assert 'valid_logs_processed' in data, "Response missing 'valid_logs_processed'"
    assert 'dead_letters' in data, "Response missing 'dead_letters'"
    assert 'latest_entropy' in data, "Response missing 'latest_entropy'"

    assert data['valid_logs_processed'] >= 2, f"Expected at least 2 valid logs processed, got {data['valid_logs_processed']}"
    assert data['dead_letters'] >= 2, f"Expected at least 2 dead letters, got {data['dead_letters']}"

    # The last valid log sent was {"message": "A"}, entropy of "A" is 0.0
    # The first valid log sent was {"message": "AABB"}, entropy of "AABB" is 1.0
    # Assuming latest_entropy updates on each valid log, it should be 0.0
    assert abs(data['latest_entropy'] - 0.0) < 0.001, f"Expected latest_entropy to be 0.0, got {data['latest_entropy']}"