# test_final_state.py

import os
import re
import socket
import subprocess
import json
from datetime import datetime

def parse_date(date_str):
    formats = [
        "%b %d %H:%M:%S %Y",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%d %b %Y %H:%M:%S"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Could not parse date: {date_str}")

def get_anonymized_email(email):
    result = subprocess.run(
        ["/app/anonymizer", email],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def test_service_responses():
    raw_file = "/home/user/raw_syslogs.txt"
    assert os.path.exists(raw_file), f"Raw logs file missing: {raw_file}"

    # Parse raw logs
    pattern = re.compile(r"^\[(.*?)\]\s+source_ip=\S+\s+user=(\S+)\s+payload=(.*)$")

    data_by_email = {}

    with open(raw_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if not match:
                continue

            timestamp_str, email, payload = match.groups()
            dt = parse_date(timestamp_str)
            iso_ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            if email not in data_by_email:
                data_by_email[email] = []

            data_by_email[email].append((dt, iso_ts, payload))

    # Test each email
    for email, records in data_by_email.items():
        anon_email = get_anonymized_email(email)

        # Sort expected records chronologically
        records.sort(key=lambda x: x[0])

        expected_lines = [
            f"{iso_ts} | {anon_email} | {payload}"
            for dt, iso_ts, payload in records
        ]

        # Connect to service
        try:
            s = socket.create_connection(("127.0.0.1", 8333), timeout=5)
        except Exception as e:
            pytest.fail(f"Could not connect to service on 127.0.0.1:8333: {e}")

        with s:
            request = f"FETCH {anon_email}\n"
            s.sendall(request.encode('utf-8'))

            response_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk

            response_text = response_data.decode('utf-8').strip()
            actual_lines = [line.strip() for line in response_text.split('\n') if line.strip()]

            assert len(actual_lines) == len(expected_lines), \
                f"Expected {len(expected_lines)} lines for {anon_email}, got {len(actual_lines)}"

            for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
                assert actual == expected, \
                    f"Mismatch at line {i+1} for {anon_email}.\nExpected: {expected}\nActual: {actual}"