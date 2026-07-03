# test_final_state.py

import os
import csv
import socket
import subprocess
import numpy as np

def test_experiment_log():
    log_path = "/home/user/experiment.log"
    assert os.path.exists(log_path), f"Experiment log {log_path} not found."
    with open(log_path, "r") as f:
        content = f.read()
    assert "Run complete: 5 records processed" in content, "Experiment log does not contain the expected success message."

def test_reduced_csv():
    reduced_path = "/home/user/reduced.csv"
    assert os.path.exists(reduced_path), f"Reduced CSV {reduced_path} not found."

    with open(reduced_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 6, f"Expected 6 rows in reduced.csv, found {len(rows)}."
    assert rows[0] == ["id", "pca1", "pca2"], f"Expected header ['id', 'pca1', 'pca2'], found {rows[0]}."

    # Check that the rest are numbers
    for i, row in enumerate(rows[1:], start=1):
        assert len(row) == 3, f"Row {i} does not have 3 columns."
        assert row[0] == str(i), f"Row {i} id mismatch."
        try:
            float(row[1])
            float(row[2])
        except ValueError:
            assert False, f"Row {i} contains non-float values for PCA components."

def test_tcp_server_serving():
    host = "127.0.0.1"
    port = 8888
    query = "test query\n"

    try:
        s = socket.create_connection((host, port), timeout=5)
        s.sendall(query.encode("utf-8"))
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        s.close()
    except Exception as e:
        assert False, f"Failed to connect and read from TCP server on {host}:{port}: {e}"

    response_str = response.decode("utf-8").strip()

    # Get expected output from binary
    binary_path = "/app/query_embedder"
    assert os.path.exists(binary_path), f"Binary {binary_path} not found."

    proc = subprocess.run(
        [binary_path],
        input=query.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    expected_str = proc.stdout.decode("utf-8").strip()

    assert response_str == expected_str, f"TCP server response does not match binary output.\nExpected: {expected_str}\nGot: {response_str}"