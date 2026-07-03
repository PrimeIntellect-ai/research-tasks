# test_final_state.py
import socket
import requests
import pytest

def test_tcp_status_endpoint():
    """Test the TCP server on port 8081."""
    host = '127.0.0.1'
    port = 8081
    message = b"STATUS auth_token=secret_123\n"

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(message)
            response = s.recv(1024)
            assert response == b"OK\n", f"Expected 'OK\\n', got {response!r}"
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to TCP server on {host}:{port}")
    except socket.timeout:
        pytest.fail("TCP server connection or read timed out")

def test_http_clean_endpoint():
    """Test the HTTP server on port 8080 for data cleaning."""
    url = 'http://127.0.0.1:8080/clean'
    payload = {
        "data": [
            [10.0, 10.0, 0.1],
            [10.1, 9.9, 0.2],
            [10.2, 10.1, -0.1],
            [100.0, -50.0, 5.0]
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        result = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "cleaned_data" in result, "Response JSON missing 'cleaned_data' key"

    cleaned_data = result["cleaned_data"]
    assert isinstance(cleaned_data, list), "cleaned_data must be a list"

    # The outlier [100.0, -50.0, 5.0] should be dropped, leaving 3 records.
    assert len(cleaned_data) == 3, f"Expected 3 records after anomaly removal, got {len(cleaned_data)}"

    # The dimensionality should be reduced to 2.
    for row in cleaned_data:
        assert len(row) == 2, f"Expected each record to have 2 dimensions, got {len(row)} for {row}"