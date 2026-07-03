# test_final_state.py

import os
import socket
import struct
import pytest

def test_harness_compiled():
    """Verify that the harness was successfully compiled."""
    harness_path = "/home/user/fuzzer/harness"
    assert os.path.exists(harness_path), f"Missing compiled harness at {harness_path}"
    assert os.path.isfile(harness_path), f"{harness_path} is not a file"
    assert os.access(harness_path, os.X_OK), f"{harness_path} is not executable"

def test_crash_payload_contents():
    """Verify the crash payload is correctly formatted to trigger the overflow."""
    payload_path = "/home/user/crash_payload.bin"
    assert os.path.exists(payload_path), f"Missing crash payload at {payload_path}"

    with open(payload_path, "rb") as f:
        data = f.read()

    assert len(data) >= 73, f"Crash payload is too short ({len(data)} bytes). Needs to be at least 73 bytes to trigger overflow."

    magic = data[0:4]
    cmd = struct.unpack(">H", data[4:6])[0]
    length = struct.unpack(">H", data[6:8])[0]

    assert magic == b"SECU", f"Invalid magic bytes in payload: {magic}"
    assert cmd == 3, f"Invalid command ID in payload: {cmd} (Expected 3 for DATA)"
    assert length > 64, f"Payload length field is {length}, must be > 64 to trigger overflow."
    assert len(data) >= 8 + length, "Payload file size does not match the length field specified in the header."

def test_mock_service_ping():
    """Verify the mock service responds correctly to the PING command."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", 9090))
        # Send PING: Magic(4), Cmd(2), Len(2)
        req = b"SECU" + struct.pack(">H", 1) + struct.pack(">H", 0)
        s.sendall(req)

        resp = s.recv(1024)
        assert len(resp) >= 8, "Response too short"
        magic = resp[0:4]
        cmd = struct.unpack(">H", resp[4:6])[0]
        length = struct.unpack(">H", resp[6:8])[0]
        payload = resp[8:8+length]

        assert magic == b"SECU", f"Invalid magic in response: {magic}"
        assert cmd == 1, f"Invalid command in response: {cmd}"
        assert payload == b"PONG", f"Invalid payload in response: {payload}"
    except ConnectionRefusedError:
        pytest.fail("Mock service is not listening on 127.0.0.1:9090")
    finally:
        s.close()

def test_mock_service_auth():
    """Verify the mock service responds correctly to the AUTH command."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", 9090))
        # Send AUTH: Magic(4), Cmd(2), Len(2), Payload("secret_token_99")
        token = b"secret_token_99"
        req = b"SECU" + struct.pack(">H", 2) + struct.pack(">H", len(token)) + token
        s.sendall(req)

        resp = s.recv(1024)
        assert len(resp) >= 8, "Response too short"
        magic = resp[0:4]
        cmd = struct.unpack(">H", resp[4:6])[0]
        length = struct.unpack(">H", resp[6:8])[0]
        payload = resp[8:8+length]

        assert magic == b"SECU", f"Invalid magic in response: {magic}"
        assert cmd == 2, f"Invalid command in response: {cmd}"
        assert payload == b"OK", f"Invalid payload in response: {payload}"
    finally:
        s.close()

def test_mock_service_handles_overflow_payload():
    """Verify the mock service does not crash when sent the overflow payload."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", 9090))
        # Send DATA command with large payload
        payload_data = b"A" * 65
        req = b"SECU" + struct.pack(">H", 3) + struct.pack(">H", len(payload_data)) + payload_data
        s.sendall(req)

        # The mock service should not crash. It might send an error or just keep the connection open.
        try:
            resp = s.recv(1024)
            # If it returns a response, it should be a valid protocol frame (e.g. an error)
            if len(resp) > 0:
                assert len(resp) >= 8, "Response too short"
                assert resp[0:4] == b"SECU", "Response does not start with SECU magic"
        except socket.timeout:
            # Timeout is acceptable if it just drops the invalid packet without crashing
            pass

        # Verify connection is still alive by sending a PING
        req_ping = b"SECU" + struct.pack(">H", 1) + struct.pack(">H", 0)
        s.sendall(req_ping)
        resp_ping = s.recv(1024)
        assert len(resp_ping) >= 8, "Service died or failed to respond to PING after malicious payload"
        assert resp_ping[8:12] == b"PONG", "Service did not respond with PONG to follow-up PING"

    finally:
        s.close()