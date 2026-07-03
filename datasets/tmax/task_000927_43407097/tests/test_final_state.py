# test_final_state.py

import socket
import os
import glob
import pytest
import threading
import re

HOST = '127.0.0.1'
PORT = 9000

def get_log_dates():
    logs_dir = '/home/user/logs'
    log_files = glob.glob(os.path.join(logs_dir, 'app_*.log'))
    dates = []
    for lf in log_files:
        m = re.search(r'app_(\d{4}-\d{2}-\d{2})\.log', lf)
        if m:
            dates.append(m.group(1))
    return sorted(dates)

def get_expected_critical_records(date):
    log_file = f'/home/user/logs/app_{date}.log'
    if not os.path.exists(log_file):
        return ""

    with open(log_file, 'r') as f:
        content = f.read()

    records = []
    current_record = []
    in_record = False
    is_critical = False

    for line in content.splitlines(True):
        if line.strip() == "--- RECORD START ---":
            in_record = True
            current_record = [line]
            is_critical = False
        elif in_record:
            current_record.append(line)
            if line.strip() == "LEVEL: CRITICAL":
                is_critical = True
            elif line.strip() == "--- RECORD END ---":
                in_record = False
                if is_critical:
                    records.append("".join(current_record))

    return "".join(records)

def send_request(date):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((HOST, PORT))
        s.sendall(f"ARCHIVE {date}\n".encode())

        header = b""
        while b"\n" not in header:
            chunk = s.recv(1)
            if not chunk:
                break
            header += chunk
            if len(header) > 100:
                break

        if not header.endswith(b"\n"):
            return None, b"Connection closed or no newline in header"

        header_str = header.decode().strip()
        if header_str.startswith("ERROR"):
            return header_str, b""

        if not header_str.startswith("SUCCESS"):
            return header_str, b""

        parts = header_str.split()
        if len(parts) != 2:
            return header_str, b"Invalid SUCCESS format"

        size = int(parts[1])

        payload = b""
        while len(payload) < size:
            chunk = s.recv(size - len(payload))
            if not chunk:
                break
            payload += chunk

        return header_str, payload
    except Exception as e:
        return "EXCEPTION", str(e).encode()
    finally:
        s.close()

def decrypt_payload(payload):
    if len(payload) < 4:
        return False, b"Payload too short"
    if payload[:4] != b"ARC1":
        return False, b"Missing ARC1 header"

    decrypted = bytearray()
    for byte in payload[4:]:
        decrypted.append(byte ^ 0x4B)
    return True, bytes(decrypted)

def test_service_listening():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        result = s.connect_ex((HOST, PORT))
        assert result == 0, f"Service is not listening on {HOST}:{PORT}"
    finally:
        s.close()

def test_not_found():
    header, payload = send_request("2099-01-01")
    assert header == "ERROR NOT_FOUND", f"Expected ERROR NOT_FOUND, got {header}"

def test_valid_archive():
    dates = get_log_dates()
    assert len(dates) > 0, "No log dates found to test"

    date = dates[0]
    expected_records = get_expected_critical_records(date)

    header, payload = send_request(date)
    assert header is not None, "Failed to get response"
    assert header.startswith("SUCCESS"), f"Expected SUCCESS, got {header}"

    parts = header.split()
    assert len(payload) == int(parts[1]), "Payload size does not match header"

    success, decrypted = decrypt_payload(payload)
    assert success, f"Decryption failed: {decrypted.decode(errors='ignore')}"

    assert decrypted.decode() == expected_records, "Decrypted payload does not match expected CRITICAL records"

def test_concurrent_requests():
    dates = get_log_dates()
    assert len(dates) > 0, "No log dates found to test"

    results = []

    def worker(date):
        header, payload = send_request(date)
        results.append((date, header, payload))

    threads = []
    # Test with 5 concurrent requests (using available dates, repeating if necessary)
    for i in range(5):
        date = dates[i % len(dates)]
        t = threading.Thread(target=worker, args=(date,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(results) == 5, "Not all threads completed"

    for date, header, payload in results:
        assert header is not None, "Failed to get response in concurrent test"
        assert header.startswith("SUCCESS"), f"Expected SUCCESS in concurrent test, got {header}"

        success, decrypted = decrypt_payload(payload)
        assert success, "Decryption failed in concurrent test"

        expected = get_expected_critical_records(date)
        assert decrypted.decode() == expected, f"Data mismatch for {date} in concurrent test. flock might not be implemented correctly."

def test_server_log():
    log_path = '/home/user/server.log'
    assert os.path.exists(log_path), f"Server log {log_path} does not exist"

    with open(log_path, 'r') as f:
        content = f.read()

    # Check format: [YYYY-MM-DD HH:MM:SS] REQUESTED: <YYYY-MM-DD> - STATUS: <SUCCESS|ERROR>
    lines = content.strip().split('\n')
    assert len(lines) > 0, "Server log is empty"

    pattern = re.compile(r'^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] REQUESTED: \d{4}-\d{2}-\d{2} - STATUS: (SUCCESS|ERROR)$')
    for line in lines:
        assert pattern.match(line), f"Invalid log line format: {line}"