# test_final_state.py

import os
import socket
import pytest

def test_libcurvefit_compiled():
    """Test that the shared library was compiled."""
    lib_path = "/app/libcurvefit-1.0/libcurvefit.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not found. Did you compile it?"

def test_tcp_server_protocol():
    """Test that the TCP server is running and implements the correct protocol."""
    host = "127.0.0.1"
    port = 8080

    # Prepare data
    # Curve 0: jump at index 45. max_idx = 45 -> Tm = 20 + 45 - 0.5 = 64.50
    curve0 = [0.1] * 100
    for i in range(45, 100):
        curve0[i] = 1.0

    # Curve 1: jump at index 60. max_idx = 60 -> Tm = 20 + 60 - 0.5 = 79.50
    curve1 = [0.1] * 100
    for i in range(60, 100):
        curve1[i] = 1.0

    # Curve 2: jump at index 20. max_idx = 20 -> Tm = 20 + 20 - 0.5 = 39.50
    curve2 = [0.1] * 100
    for i in range(20, 100):
        curve2[i] = 1.0

    payload = "3\n"
    payload += " ".join(f"{x:.2f}" for x in curve0) + "\n"
    payload += " ".join(f"{x:.2f}" for x in curve1) + "\n"
    payload += " ".join(f"{x:.2f}" for x in curve2) + "\n"

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(payload.encode('utf-8'))

            # Read response
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data
                if response.decode('utf-8').count('\n') >= 3:
                    break
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to TCP server at {host}:{port}. Is it running?")
    except socket.timeout:
        pytest.fail(f"Connection to TCP server at {host}:{port} timed out.")

    response_str = response.decode('utf-8').strip()
    lines = response_str.split('\n')

    assert len(lines) == 3, f"Expected 3 lines of output, got {len(lines)}. Response: {response_str}"

    assert "Curve 0: Tm = 64.50" in lines[0], f"Expected Curve 0 Tm to be 64.50, got: {lines[0]}"
    assert "Curve 1: Tm = 79.50" in lines[1], f"Expected Curve 1 Tm to be 79.50, got: {lines[1]}"
    assert "Curve 2: Tm = 39.50" in lines[2], f"Expected Curve 2 Tm to be 39.50, got: {lines[2]}"