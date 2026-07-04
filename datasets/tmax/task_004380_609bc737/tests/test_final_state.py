# test_final_state.py
import os
import csv
import requests
import pytest

def test_archive_server_binary_exists():
    path = "/usr/local/bin/archive_server"
    assert os.path.exists(path), f"Binary {path} does not exist. Did you compile your C++ code to this location?"
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def get_expected_files():
    csv_path = "/var/backups/production.csv"
    dat_path = "/var/backups/production.dat"

    assert os.path.exists(csv_path), f"Missing {csv_path}"
    assert os.path.exists(dat_path), f"Missing {dat_path}"

    files = {}
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 3:
                continue
            filename, offset, length = row[0], int(row[1]), int(row[2])
            files[filename] = (offset, length)

    expected_contents = {}
    with open(dat_path, 'rb') as f:
        for filename, (offset, length) in files.items():
            f.seek(offset)
            data = f.read(length)
            plaintext = bytes([b ^ 0x5A for b in data])
            expected_contents[filename] = plaintext

    return expected_contents

def test_http_service_valid_files():
    expected_contents = get_expected_files()
    assert expected_contents, "No files found in the production archive to test."

    for filename, expected_data in expected_contents.items():
        url = f"http://127.0.0.1:9000/file/{filename}"
        try:
            response = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the HTTP service at {url}. Is the server running? Error: {e}")

        assert response.status_code == 200, f"Expected status code 200 for {filename}, got {response.status_code}"
        assert response.content == expected_data, f"Content mismatch for {filename}. Expected {expected_data}, got {response.content}"

def test_http_service_nonexistent_file():
    url = "http://127.0.0.1:9000/file/this_file_does_not_exist_12345.txt"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service at {url}. Is the server running? Error: {e}")

    assert response.status_code == 404, f"Expected status code 404 for nonexistent file, got {response.status_code}"