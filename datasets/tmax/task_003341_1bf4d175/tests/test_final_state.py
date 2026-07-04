# test_final_state.py

import os
import struct
import requests
import socket
import pytest

def get_all_records():
    """Parse all WAL files to extract records."""
    records = {}
    wal_dir = "/app/wal_data"
    if not os.path.isdir(wal_dir):
        return records

    for fname in os.listdir(wal_dir):
        fpath = os.path.join(wal_dir, fname)
        if os.path.isfile(fpath) and not os.path.islink(fpath) and fname.endswith(".wal"):
            with open(fpath, "rb") as f:
                while True:
                    header = f.read(4)
                    if not header:
                        break
                    if header != b"WALR":
                        break
                    meta = f.read(8)
                    if len(meta) < 8:
                        break
                    rec_id, length = struct.unpack("<II", meta)
                    payload = f.read(length)
                    if len(payload) < length:
                        break
                    records[rec_id] = payload.decode('ascii')
    return records

def test_archive_service_files_exist():
    """Check if the C++ source and binary exist."""
    assert os.path.isfile("/home/user/archive_service.cpp"), "Source file /home/user/archive_service.cpp is missing."
    assert os.path.isfile("/home/user/archive_service"), "Compiled binary /home/user/archive_service is missing."
    assert os.access("/home/user/archive_service", os.X_OK), "/home/user/archive_service is not executable."

def test_services_listening():
    """Check if ports 8000 (nginx) and 8080 (C++ service) are open."""
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    assert is_port_open(8000), "Nginx is not listening on port 8000."
    assert is_port_open(8080), "C++ archive service is not listening on port 8080."

def test_nginx_proxy_valid_records():
    """Test that nginx correctly proxies valid record requests to the C++ service."""
    records = get_all_records()
    assert records, "No records found in WAL files to test against."

    # Test a few records
    test_ids = list(records.keys())[:5]
    for rec_id in test_ids:
        expected_payload = records[rec_id]
        url = f"http://127.0.0.1:8000/api/record/{rec_id}"

        try:
            response = requests.get(url, timeout=2)
        except requests.RequestException as e:
            pytest.fail(f"Request to {url} failed: {e}")

        assert response.status_code == 200, f"Expected status 200 for record {rec_id}, got {response.status_code}"
        assert response.text == expected_payload, f"Payload mismatch for record {rec_id}. Expected '{expected_payload}', got '{response.text}'"

def test_nginx_proxy_invalid_record():
    """Test that requesting a non-existent record returns 404."""
    records = get_all_records()
    # Find an ID that definitely doesn't exist
    invalid_id = 99999999
    while invalid_id in records:
        invalid_id += 1

    url = f"http://127.0.0.1:8000/api/record/{invalid_id}"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 404, f"Expected status 404 for invalid record {invalid_id}, got {response.status_code}"