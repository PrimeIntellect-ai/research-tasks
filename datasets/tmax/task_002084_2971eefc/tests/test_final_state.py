# test_final_state.py
import os
import re
import socket
import json
import csv

def test_pipeline_log_exists_and_format():
    log_path = '/home/user/pipeline.log'
    assert os.path.exists(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    pattern = r'^Processed \d+ raw frames, saved \d+ cleaned frames\.$'
    assert re.match(pattern, content), f"Log file content '{content}' does not match expected format."

def test_cleaned_data_csv_exists_and_format():
    csv_path = '/home/user/cleaned_data.csv'
    assert os.path.exists(csv_path), f"CSV file {csv_path} is missing."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['timestamp_ms', 'brightness'], f"CSV header {header} is incorrect."

        for row in reader:
            assert len(row) == 2, f"CSV row {row} does not have exactly 2 columns."
            assert row[0].isdigit(), f"Timestamp '{row[0]}' is not an integer."
            assert row[1].isdigit(), f"Brightness '{row[1]}' is not an integer."

def test_tcp_server_response():
    host = '127.0.0.1'
    port = 9000

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b'FETCH_SERIES\n')

            # Read all response data
            response_bytes = b''
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_bytes += chunk
    except ConnectionRefusedError:
        assert False, f"TCP server is not listening on {host}:{port}."
    except Exception as e:
        assert False, f"Error communicating with TCP server: {e}"

    assert response_bytes, "TCP server returned empty response."

    try:
        response_str = response_bytes.decode('utf-16le')
    except UnicodeDecodeError:
        assert False, "Response is not valid UTF-16LE encoded."

    try:
        data = json.loads(response_str)
    except json.JSONDecodeError:
        assert False, f"Decoded response is not valid JSON: {response_str}"

    assert isinstance(data, list), "JSON response should be a list of objects."

    # Read CSV to compare
    csv_path = '/home/user/cleaned_data.csv'
    csv_data = []
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_data.append({"t": int(row['timestamp_ms']), "v": int(row['brightness'])})

    assert data == csv_data, "JSON response data does not match CSV data."