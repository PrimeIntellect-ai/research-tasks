# test_final_state.py
import socket
import subprocess
import math
import pytest

def get_oracle_output(text):
    result = subprocess.run(["/app/embedding_oracle", text], capture_output=True, text=True, check=True)
    return [float(x) for x in result.stdout.strip().split()]

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x) ** 2 for xi in x)
    den_y = sum((yi - mean_y) ** 2 for yi in y)
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / math.sqrt(den_x * den_y)

def send_recv(sock, msg):
    sock.sendall(msg.encode('utf-8'))
    resp = b""
    while not resp.endswith(b"\n"):
        chunk = sock.recv(1024)
        if not chunk:
            break
        resp += chunk
    return resp.decode('utf-8')

def test_tcp_server_protocol():
    host = "127.0.0.1"
    port = 9000

    try:
        s = socket.create_connection((host, port), timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to connect to {host}:{port}. Error: {e}")

    with s:
        # Test 1: Length < 8
        resp = send_recv(s, "EMBED abc\n")
        assert resp == "ERROR_SCHEMA\n", f"Expected ERROR_SCHEMA\\n, got {resp!r}"

        # Test 2: Non-alphanumeric
        resp = send_recv(s, "EMBED abcdefgh!@\n")
        assert resp == "ERROR_SCHEMA\n", f"Expected ERROR_SCHEMA\\n, got {resp!r}"

        # Test 3: Valid text 1
        resp = send_recv(s, "EMBED abcdefgh\n")
        assert resp == "OK 0\n", f"Expected OK 0\\n, got {resp!r}"

        # Test 4: Valid text 2
        resp = send_recv(s, "EMBED 12345678\n")
        assert resp == "OK 1\n", f"Expected OK 1\\n, got {resp!r}"

        # Test 5: Correlate valid indices
        vec0 = get_oracle_output("abcdefgh")
        vec1 = get_oracle_output("12345678")
        expected_corr = pearson_correlation(vec0, vec1)
        expected_resp = f"{expected_corr:.4f}\n"

        resp = send_recv(s, "CORRELATE 0 1\n")
        assert resp == expected_resp, f"Expected {expected_resp!r}, got {resp!r}"

        # Test 6: Correlate invalid index
        resp = send_recv(s, "CORRELATE 0 99\n")
        assert resp == "ERROR_NOT_FOUND\n", f"Expected ERROR_NOT_FOUND\\n, got {resp!r}"

        # Test 7: EXIT
        resp = send_recv(s, "EXIT\n")
        assert resp == "GOODBYE\n", f"Expected GOODBYE\\n, got {resp!r}"

        # Check connection is closed
        try:
            s.settimeout(1)
            chunk = s.recv(1024)
            assert chunk == b"", "Connection should be closed after EXIT"
        except socket.timeout:
            pytest.fail("Connection was not closed after EXIT command")
        except socket.error:
            pass # Socket closed as expected