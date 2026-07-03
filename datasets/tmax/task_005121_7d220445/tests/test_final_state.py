# test_final_state.py
import socket
import os
import time
import pytest

def run_protocol(port, metric_name, metric_value):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect(('127.0.0.1', port))

        s.sendall(b"HELO PROBE_SYS_v2\n")
        resp = s.recv(1024)
        assert resp == b"OK READY\n", f"Expected 'OK READY\\n', got {resp!r} on port {port}"

        metric_msg = f"METRIC {metric_name} {metric_value}\n".encode()
        s.sendall(metric_msg)
        resp = s.recv(1024)
        expected_ack = f"ACK {metric_name}\n".encode()
        assert resp == expected_ack, f"Expected {expected_ack!r}, got {resp!r} on port {port}"

        s.sendall(b"BYE\n")
        resp = s.recv(1024)
        assert resp == b"", f"Expected connection close after BYE, got {resp!r} on port {port}"

        s.close()
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused on port {port}. Is the service/tunnel running?")
    except socket.timeout:
        pytest.fail(f"Socket timeout while communicating on port {port}.")

def test_receiver_protocol_9090():
    """Verify the protocol directly on the receiver port 9090."""
    run_protocol(9090, "TEST_MEM", "2048")

def test_tunnel_protocol_8080():
    """Verify the protocol through the SSH tunnel on port 8080."""
    run_protocol(8080, "TEST_CPU", "99")

def test_alerts_log():
    """Verify that the alerts log contains the correctly formatted alerts."""
    log_path = "/home/user/alerts.log"
    assert os.path.exists(log_path), f"Alerts log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "[ALERT_RECEIVED] TEST_MEM: 2048" in content, "Log file missing expected entry for TEST_MEM."
    assert "[ALERT_RECEIVED] TEST_CPU: 99" in content, "Log file missing expected entry for TEST_CPU."