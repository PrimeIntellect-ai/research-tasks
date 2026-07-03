# test_final_state.py

import socket
import pytest

def test_ports_open():
    """Verify that both ingest service and DB service are listening."""
    for port in [8000, 8001]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"Port {port} is not open. Ensure both services are started in the background."

def send_payload(payload):
    """Helper to send a payload to the ingest service and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        try:
            s.connect(('127.0.0.1', 8000))
            s.sendall(payload.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
        except Exception as e:
            pytest.fail(f"Failed to communicate with ingest service on port 8000: {e}")

def test_valid_request():
    """Test a normal, healthy metric payload."""
    payload = "METRIC webapp 80 40\n"
    resp = send_payload(payload)
    assert resp == "OK\n", f"Expected 'OK\\n' for valid payload, got {repr(resp)}"

def test_corrupted_input():
    """Test a payload with a carriage return injected."""
    payload = "METRIC cache 50\r 60\n"
    resp = send_payload(payload)
    assert resp == "OK\n", f"Expected 'OK\\n' for carriage-return payload, got {repr(resp)}. Ensure ingest_handler.sh strips \\r."

def test_edge_case_format():
    """Test a payload with a non-numeric memory value."""
    payload = "METRIC worker 90 NaN\n"
    resp = send_payload(payload)
    assert resp == "OK\n", f"Expected 'OK\\n' for non-numeric memory payload, got {repr(resp)}. Ensure db_handler.sh defaults non-numeric mem to 0."

def test_corrupted_and_edge_case():
    """Test a payload with both carriage return and non-numeric memory value."""
    payload = "METRIC DB 75\r N/A\n"
    resp = send_payload(payload)
    assert resp == "OK\n", f"Expected 'OK\\n' for combined corrupted/edge-case payload, got {repr(resp)}."