# test_final_state.py
import os
import socket
import ssl
import time
import pytest

def test_phase1_certificates_exist():
    """Test that the TLS certificates were generated in the correct directory."""
    cert_dir = "/home/user/audit_certs"
    key_file = os.path.join(cert_dir, "server.key")
    crt_file = os.path.join(cert_dir, "server.crt")

    assert os.path.isdir(cert_dir), f"Directory {cert_dir} does not exist."
    assert os.path.isfile(key_file), f"Private key {key_file} does not exist."
    assert os.path.isfile(crt_file), f"Certificate {crt_file} does not exist."

def test_phase3_historical_decryption():
    """Test that the historical traffic was correctly decrypted."""
    audit_file = "/home/user/historical_audit.txt"
    assert os.path.isfile(audit_file), f"Decrypted file {audit_file} does not exist."

    with open(audit_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected = "AUDIT_START: System initialized securely."
    assert content == expected, f"Expected historical audit content to be '{expected}', but got '{content}'."

def test_phase4_secure_audit_proxy():
    """Test that the secure audit listener is running, accepts TLS connections, decrypts data, and logs it."""
    a = 11
    b = 85
    msg = b"LIVE_AUDIT_TEST_PROBE"
    enc_msg = bytes([(a * p + b) % 256 for p in msg])

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection(("127.0.0.1", 8443), timeout=2) as sock:
            with ctx.wrap_socket(sock, server_hostname="localhost") as ssock:
                ssock.write(enc_msg)
    except ConnectionRefusedError:
        pytest.fail("Connection refused on 127.0.0.1:8443. Is the secure_audit_listener.py running?")
    except ssl.SSLError as e:
        pytest.fail(f"SSL error during connection. Is the listener using TLS? Error: {e}")
    except Exception as e:
        pytest.fail(f"Failed to connect to the live audit proxy: {e}")

    # Give the server a moment to process and write to the log
    time.sleep(1)

    log_file = "/home/user/live_audit.log"
    assert os.path.isfile(log_file), f"Live audit log file {log_file} does not exist."

    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "LIVE_AUDIT_TEST_PROBE" in log_content, "The live audit proxy did not log the decrypted test message."