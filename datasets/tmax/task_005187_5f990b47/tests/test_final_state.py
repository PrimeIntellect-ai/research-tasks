# test_final_state.py
import socket
import re
import pytest

def test_service_eval_700():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(('127.0.0.1', 9000))
    except Exception as e:
        pytest.fail(f"Could not connect to service on 127.0.0.1:9000: {e}")

    try:
        s.sendall(b'EVAL 700\n')
        data = s.recv(1024).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Error communicating with service: {e}")
    finally:
        s.close()

    if not re.match(r"^CI: -?\d+\.\d{4}, -?\d+\.\d{4}\n$", data):
        pytest.fail(f"Invalid response format: {repr(data)}")

    parts = data.strip().split()
    lower, upper = [float(x.strip(',')) for x in parts[1:]]

    if not (-0.5 < lower < 0.1):
        pytest.fail(f"Lower bound {lower} out of expected range (-0.5, 0.1)")
    if not (-0.1 < upper < 0.5):
        pytest.fail(f"Upper bound {upper} out of expected range (-0.1, 0.5)")
    if lower >= upper:
        pytest.fail(f"Lower bound ({lower}) must be strictly less than upper bound ({upper})")

def test_service_eval_500():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(('127.0.0.1', 9000))
    except Exception as e:
        pytest.fail(f"Could not connect to service on 127.0.0.1:9000: {e}")

    try:
        s.sendall(b'EVAL 500\n')
        data = s.recv(1024).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Error communicating with service: {e}")
    finally:
        s.close()

    if not re.match(r"^CI: -?\d+\.\d{4}, -?\d+\.\d{4}\n$", data):
        pytest.fail(f"Invalid response format: {repr(data)}")

    parts = data.strip().split()
    lower, upper = [float(x.strip(',')) for x in parts[1:]]

    if not (-0.5 < lower < 0.2):
        pytest.fail(f"Lower bound {lower} out of expected range for EVAL 500")
    if not (-0.2 < upper < 0.5):
        pytest.fail(f"Upper bound {upper} out of expected range for EVAL 500")
    if lower >= upper:
        pytest.fail(f"Lower bound ({lower}) must be strictly less than upper bound ({upper})")