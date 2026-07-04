# test_final_state.py

import os
import socket
import struct
import base64
import time
import threading
import subprocess
import pytest

def encode_payload(data: bytes) -> bytes:
    xored = bytes(b ^ 0x5A for b in data)
    b64 = base64.b64encode(xored)
    return struct.pack('>I', len(b64)) + b64

def test_proxy_exists():
    assert os.path.exists("/home/user/proxy.py"), "Proxy script /home/user/proxy.py does not exist."

def test_proxy_f1_score():
    # Kill any existing consumer on port 8001 to mock it
    subprocess.run(["fuser", "-k", "8001/tcp"], capture_output=True)
    time.sleep(1)

    received_payloads = []
    stop_event = threading.Event()

    def consumer_thread():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(('127.0.0.1', 8001))
                s.listen(5)
                s.settimeout(1.0)
            except Exception:
                return

            while not stop_event.is_set():
                try:
                    conn, addr = s.accept()
                    with conn:
                        conn.settimeout(1.0)
                        while not stop_event.is_set():
                            try:
                                header = conn.recv(4)
                                if not header or len(header) < 4:
                                    break
                                length = struct.unpack('>I', header)[0]
                                data = b""
                                while len(data) < length:
                                    chunk = conn.recv(length - len(data))
                                    if not chunk:
                                        break
                                    data += chunk
                                if len(data) == length:
                                    received_payloads.append(data)
                            except socket.timeout:
                                continue
                            except Exception:
                                break
                except socket.timeout:
                    continue
                except Exception:
                    break

    t = threading.Thread(target=consumer_thread)
    t.start()
    time.sleep(1)

    malicious = b"SYSTEM_INIT_CRASH_OVERRIDE_V1_TRIGGER"
    benign = b"SENSOR_DATA_99.8_OK"

    num_benign = 100
    num_malicious = 20

    try:
        # Send payloads to the proxy on port 8000
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect(('127.0.0.1', 8000))

            for _ in range(num_benign):
                s.sendall(encode_payload(benign))
                time.sleep(0.01)

            for _ in range(num_malicious):
                s.sendall(encode_payload(malicious))
                time.sleep(0.01)

    except ConnectionRefusedError:
        stop_event.set()
        t.join()
        pytest.fail("Connection to proxy on 127.0.0.1:8000 was refused. Is the proxy running?")
    except Exception as e:
        stop_event.set()
        t.join()
        pytest.fail(f"Error communicating with proxy: {e}")

    time.sleep(1)
    stop_event.set()
    t.join()

    expected_benign_b64 = base64.b64encode(bytes(b ^ 0x5A for b in benign))
    expected_malicious_b64 = base64.b64encode(bytes(b ^ 0x5A for b in malicious))

    benign_received = sum(1 for p in received_payloads if p == expected_benign_b64)
    malicious_received = sum(1 for p in received_payloads if p == expected_malicious_b64)

    # True Positives = Dropped Malicious
    tp = num_malicious - malicious_received
    # False Positives = Dropped Benign
    fp = num_benign - benign_received
    # False Negatives = Forwarded Malicious
    fn = malicious_received

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    assert f1 >= 0.99, f"F1 score {f1:.4f} is below threshold 0.99. TP={tp}, FP={fp}, FN={fn}. Benign received: {benign_received}/{num_benign}, Malicious received: {malicious_received}/{num_malicious}."