# test_final_state.py

import os
import socket
import time
import requests
import pytest

def test_http_service():
    """Verify that the HTTP service is running and returns the correct response for the profile."""
    url = "http://127.0.0.1:8080/profile/charlie"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    expected_body = "User: charlie, Secret: ocean"
    assert response.text.strip() == expected_body, f"Expected body '{expected_body}', got '{response.text}'"

def test_smtp_service():
    """Verify that the SMTP service is running, accepts standard commands, and logs the message."""
    host = "127.0.0.1"
    port = 8025

    try:
        s = socket.create_connection((host, port), timeout=5)
    except OSError as e:
        pytest.fail(f"Failed to connect to SMTP service at {host}:{port}: {e}")

    with s:
        # Read greeting
        s.recv(1024)

        def send_cmd(cmd):
            s.sendall(cmd.encode() + b"\r\n")
            time.sleep(0.1)
            resp = s.recv(1024).decode()
            return resp

        resp = send_cmd("HELO verifier")
        assert resp.startswith("2"), f"Expected 2xx response for HELO, got: {resp}"

        resp = send_cmd("MAIL FROM:<admin@localhost>")
        assert resp.startswith("2"), f"Expected 2xx response for MAIL FROM, got: {resp}"

        resp = send_cmd("RCPT TO:<charlie@localhost>")
        assert resp.startswith("2"), f"Expected 2xx response for RCPT TO, got: {resp}"

        resp = send_cmd("DATA")
        assert resp.startswith("354"), f"Expected 354 response for DATA, got: {resp}"

        test_msg = "Subject: Test\n\nThis is a test message from the verifier."
        s.sendall(test_msg.encode() + b"\r\n.\r\n")
        time.sleep(0.2)
        resp = s.recv(1024).decode()
        assert resp.startswith("2"), f"Expected 2xx response after DATA payload, got: {resp}"

        send_cmd("QUIT")

    # Check that the test message was written to mail.log
    log_path = "/home/user/mail.log"
    assert os.path.isfile(log_path), f"mail.log was not created at {log_path}"

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "This is a test message from the verifier." in log_content, "The test message body was not found in mail.log"

def test_welcome_email_sent():
    """Verify that an initial welcome email was sent and logged."""
    log_path = "/home/user/mail.log"
    assert os.path.isfile(log_path), f"mail.log is missing at {log_path}, meaning no welcome email was logged."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert len(log_content.strip()) > 0, "mail.log is empty. Expected an initial welcome email to be logged."