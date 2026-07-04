# test_final_state.py
import os
import csv
import socket
import tempfile
import subprocess
import pytest

def generate_csv(path, data):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "value"])
        for row in data:
            writer.writerow(row)

def check_server_with_data(data1, data2):
    fd1, path1 = tempfile.mkstemp(suffix=".csv")
    fd2, path2 = tempfile.mkstemp(suffix=".csv")
    os.close(fd1)
    os.close(fd2)

    generate_csv(path1, data1)
    generate_csv(path2, data2)

    try:
        # Run oracle
        proc = subprocess.run(
            ["/app/data_oracle", path1, path2],
            capture_output=True,
            text=True,
            check=True
        )
        expected = proc.stdout.strip()

        # Connect to server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        try:
            s.connect(("127.0.0.1", 9000))
        except Exception as e:
            pytest.fail(f"Could not connect to TCP server on 127.0.0.1:9000: {e}")

        # Send payload terminated by null byte
        payload = f"{path1}\n{path2}\0".encode('utf-8')
        s.sendall(payload)

        response = s.recv(1024).decode('utf-8').strip()
        s.close()

        assert response == expected, f"Expected {expected!r} but got {response!r} from server for inputs {data1} and {data2}"
    finally:
        os.remove(path1)
        os.remove(path2)

def test_server_correlation_positive():
    data1 = [("1", "10"), ("2", "20"), ("3", "30"), ("4", "40")]
    data2 = [("2", "20"), ("3", "30"), ("4", "40"), ("5", "50")]
    check_server_with_data(data1, data2)

def test_server_correlation_negative_with_floats():
    data1 = [("10", "1.5"), ("20", "2.5"), ("30", "3.5"), ("40", "4.5")]
    data2 = [("10", "10.0"), ("20", "8.0"), ("30", "6.0"), ("40", "4.0")]
    check_server_with_data(data1, data2)

def test_server_correlation_missing_data():
    data1 = [("1", "100"), ("2", "200"), ("4", "400"), ("5", "500")]
    data2 = [("2", "20"), ("3", "30"), ("4", "40"), ("6", "60")]
    check_server_with_data(data1, data2)