# test_final_state.py

import socket
import struct
import pytest

def test_c2_emulator_response():
    """Connect to the C2 emulator, send the handshake, and verify the response."""
    host = "127.0.0.1"
    port = 8080

    # Payload: "HELLO C2" XOR 42
    # "HELLO C2" -> [72, 69, 76, 76, 79, 32, 67, 50]
    # XOR 42 -> [114, 111, 102, 102, 101, 10, 105, 24] or \x62\x6f\x66\x66\x65\x0a\x69\x18
    request_payload = bytes([c ^ 42 for c in b"HELLO C2"])
    request_length = struct.pack(">I", len(request_payload))
    request_data = request_length + request_payload

    # Expected response: "WELCOME" XOR 42
    expected_payload = bytes([c ^ 42 for c in b"WELCOME"])
    expected_length = struct.pack(">I", len(expected_payload))
    expected_data = expected_length + expected_payload

    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            sock.sendall(request_data)

            # Read length prefix (4 bytes)
            resp_length_data = sock.recv(4)
            assert len(resp_length_data) == 4, f"Expected 4 bytes for length prefix, got {len(resp_length_data)} bytes."

            resp_length = struct.unpack(">I", resp_length_data)[0]
            assert resp_length == len(expected_payload), f"Expected response length {len(expected_payload)}, got {resp_length}."

            # Read payload
            resp_payload = sock.recv(resp_length)
            assert len(resp_payload) == resp_length, f"Expected {resp_length} bytes of payload, got {len(resp_payload)} bytes."

            assert resp_payload == expected_payload, f"Expected payload {expected_payload.hex()}, got {resp_payload.hex()}."

    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to C2 emulator at {host}:{port}. Is it running and listening on the correct port?")
    except socket.timeout:
        pytest.fail("Connection or read timed out. The emulator may not be responding correctly.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while communicating with the emulator: {e}")