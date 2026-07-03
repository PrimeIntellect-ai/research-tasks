# test_final_state.py

import socket
import pytest

def test_daemon_protocol():
    host = "127.0.0.1"
    port = 9090

    try:
        s = socket.create_connection((host, port), timeout=5)
    except Exception as e:
        pytest.fail(f"Could not connect to daemon at {host}:{port}. Did you start it in the background? Error: {e}")

    with s:
        # Use a file-like object for reading lines
        f = s.makefile('rw', encoding='utf-8')

        # 1. Send Auth
        f.write("AUTH x-daemon-token-99\n")
        f.flush()

        resp = f.readline()
        assert resp == "OK\n", f"Expected 'OK\\n' after AUTH, got {repr(resp)}"

        # 2. Send valid metric to test floating-point precision
        f.write("METRIC MEM 10.1 20.2 30.3\n")
        f.flush()

        resp = f.readline()
        assert resp == "AVG: 20.2000\n", f"Expected 'AVG: 20.2000\\n' for valid metric, got {repr(resp)}. Ensure 4 decimal places precision."

        # 3. Send invalid metric (NaN) to test crash fix
        f.write("METRIC CPU 100 200 NaN 300\n")
        f.flush()

        resp = f.readline()
        assert resp == "ERROR: BAD INPUT\n", f"Expected 'ERROR: BAD INPUT\\n' for NaN metric, got {repr(resp)}"

        # 4. Check that connection is still alive by sending another valid metric
        f.write("METRIC MEM 1 2 3\n")
        f.flush()

        try:
            resp = f.readline()
        except Exception as e:
            pytest.fail(f"Connection dropped after BAD INPUT. The server must not crash or exit. Error: {e}")

        assert resp == "AVG: 2.0000\n", f"Expected 'AVG: 2.0000\\n' after bad input to ensure connection didn't drop, got {repr(resp)}"