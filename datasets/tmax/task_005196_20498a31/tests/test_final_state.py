# test_final_state.py
import pytest
import requests
import socket
import time

HTTP_BASE_URL = "http://127.0.0.1:8080"
TCP_HOST = "127.0.0.1"
TCP_PORT = 9000

def test_http_en_greeting():
    """
    Tests deduplication: timestamp 1700000200 > 1700000000.
    Expects Welcome.
    """
    try:
        response = requests.get(f"{HTTP_BASE_URL}/translate", params={"locale": "en", "key": "greeting"}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("translation") == "Welcome", f"Expected translation 'Welcome', got {data.get('translation')}"

def test_http_eng_greeting():
    """
    Tests constraint validation: ENG dropped.
    Expects 404.
    """
    try:
        response = requests.get(f"{HTTP_BASE_URL}/translate", params={"locale": "ENG", "key": "greeting"}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert response.status_code == 404, f"Expected HTTP 404, got {response.status_code}. Response: {response.text}"

def test_http_fr_greeting_audio_override():
    """
    Tests audio transcription and TCP ingestion success.
    Expects salut.
    """
    try:
        response = requests.get(f"{HTTP_BASE_URL}/translate", params={"locale": "fr", "key": "greeting"}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("translation") == "salut", f"Expected translation 'salut', got {data.get('translation')}"

def test_tcp_ingestion_and_http_read():
    """
    Tests that the TCP ingestion port correctly processes new live data from the verifier.
    """
    # Send TCP update
    try:
        with socket.create_connection((TCP_HOST, TCP_PORT), timeout=2) as sock:
            sock.sendall(b"es:farewell:Adios\n")
    except Exception as e:
        pytest.fail(f"TCP connection or send failed: {e}")

    # Give the server a tiny moment to process the update
    time.sleep(0.1)

    # Verify via HTTP
    try:
        response = requests.get(f"{HTTP_BASE_URL}/translate", params={"locale": "es", "key": "farewell"}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("translation") == "Adios", f"Expected translation 'Adios', got {data.get('translation')}"