# test_final_state.py

import os
import time
import socket
import json
import uuid
import requests
import pytest

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val), version=4)
        return True
    except ValueError:
        return False

def test_processor_running():
    process_found = False
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            try:
                with open(f'/proc/{pid}/cmdline', 'r') as f:
                    cmdline = f.read()
                    if 'processor.py' in cmdline:
                        process_found = True
                        break
            except (IOError, OSError):
                continue
    assert process_found, "processor.py is not running in the background"

def test_tcp_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:
        sock.connect(('127.0.0.1', 9000))
    except Exception as e:
        pytest.fail(f"Failed to connect to TCP server on localhost:9000: {e}")

    sock.setblocking(False)

    start_time = time.time()
    buffer = ""
    messages = []

    while time.time() - start_time < 3.0:
        try:
            data = sock.recv(4096)
            if data:
                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        messages.append(line.strip())
            else:
                time.sleep(0.1)
        except BlockingIOError:
            time.sleep(0.1)
        except Exception as e:
            pytest.fail(f"Error reading from TCP socket: {e}")

    sock.close()

    assert len(messages) >= 5, f"Expected at least 5 CRITICAL messages over TCP, got {len(messages)}"

    for msg in messages:
        try:
            log_data = json.loads(msg)
        except json.JSONDecodeError:
            pytest.fail(f"Received invalid JSON over TCP: {msg}")

        assert 'level' in log_data, f"Log missing 'level' key: {log_data}"
        assert log_data['level'] == 'CRITICAL', f"Expected level CRITICAL, got {log_data['level']}"

        assert 'id' in log_data, f"Log missing 'id' key: {log_data}"
        assert is_valid_uuid(log_data['id']), f"Invalid UUID4 in log: {log_data['id']}"

def test_metrics_api():
    try:
        response = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to connect to API on localhost:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        metrics = response.json()
    except ValueError:
        pytest.fail("API response is not valid JSON")

    assert isinstance(metrics, dict), "Metrics response should be a JSON object"

    levels_found = set()
    for key in metrics.keys():
        assert not key.endswith('_DEBUG'), f"Found invalid level in metrics: {key}"
        assert not key.endswith('_FATAL'), f"Found invalid level in metrics: {key}"

        if key.endswith('_INFO'):
            levels_found.add('INFO')
        elif key.endswith('_WARN'):
            levels_found.add('WARN')
        elif key.endswith('_CRITICAL'):
            levels_found.add('CRITICAL')

    assert 'INFO' in levels_found, "Metrics missing INFO logs"
    assert 'WARN' in levels_found, "Metrics missing WARN logs"
    assert 'CRITICAL' in levels_found, "Metrics missing CRITICAL logs"