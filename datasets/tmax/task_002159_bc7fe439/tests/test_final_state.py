# test_final_state.py

import socket
import math
import time

def compute_expected(init_val: float) -> float:
    t = 0.0
    dt = 0.1
    val = init_val
    while t < 1.0:
        error = dt * 0.5
        if error > 0.02:
            dt /= 2.0
            continue
        val += dt * math.sin(val)
        t += dt
    return val

def test_tcp_server_response():
    host = '127.0.0.1'
    port = 8181

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)

    connected = False
    for _ in range(10):
        try:
            s.connect((host, port))
            connected = True
            break
        except Exception:
            time.sleep(0.5)

    assert connected, f"Could not connect to TCP server at {host}:{port}. Ensure the service is running in the background."

    payload = "0.2,0.8,1.5,0.7,0.1\n"
    try:
        s.sendall(payload.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
    except Exception as e:
        s.close()
        raise AssertionError(f"Failed to communicate with the server: {e}")
    finally:
        s.close()

    # 0.2 + 0.8 + 1.5 + 0.7 + 0.1 = 3.3
    expected_val = compute_expected(3.3)
    expected_response = f"RESULT: {expected_val:.4f}\n"

    assert response == expected_response, f"Server returned incorrect response. Expected {expected_response!r}, got {response!r}"