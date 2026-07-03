# test_final_state.py

import os
import socket
import pytest
import hashlib

def test_anomalies_file():
    path = "/home/user/anomalies.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split("\n") if line.strip()]
    assert len(lines) == 1, f"Expected exactly 1 anomaly line, found {len(lines)}"
    assert lines[0] == "2023-10-04T16,12", f"Incorrect anomaly data: {lines[0]}"

def test_clean_tm_file():
    path = "/home/user/clean_tm.csv"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split("\n") if line.strip()]
    assert len(lines) == 2, f"Expected exactly 2 lines in clean_tm.csv, found {len(lines)}"

    md5_hello = hashlib.md5(b"Hello World").hexdigest()
    md5_save = hashlib.md5(b"Save").hexdigest()

    expected_hello = f"{md5_hello},Salut tout le monde"
    expected_save = f"{md5_save},Enregistrer"

    assert expected_hello in lines, f"Missing or incorrect entry for 'Hello World' in clean_tm.csv"
    assert expected_save in lines, f"Missing or incorrect entry for 'Save' in clean_tm.csv"

def test_pack_bin_file():
    path = "/home/user/pack.bin"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "rb") as f:
        data = f.read()

    assert data.startswith(b"TMPK"), "pack.bin does not start with the TMPK magic header."
    assert len(data) > 4, "pack.bin contains only the magic header, no data."

def test_tcp_get_anomalies():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", 8888))
        s.sendall(b"GET_ANOMALIES\n")

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with TCP server on port 8888 for GET_ANOMALIES: {e}")

    assert b"2023-10-04T16,12" in response, f"TCP server did not return correct anomalies data. Response: {response}"

def test_tcp_get_pack():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", 8888))
        s.sendall(b"GET_PACK\n")

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with TCP server on port 8888 for GET_PACK: {e}")

    assert response.startswith(b"TMPK"), "TCP server did not return the correct pack.bin data (missing TMPK header)."
    assert len(response) > 4, "TCP server returned empty pack.bin data."