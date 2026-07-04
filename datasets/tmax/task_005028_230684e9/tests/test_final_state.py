# test_final_state.py

import os
import struct
import requests
import pytest

def create_bkp_payload():
    magic = b"BKP\x01"

    filename = b"../../../home/user/hacked.log"
    filename_len = len(filename)

    data = (
        b"=== LOG START ===\n"
        b"Date: 2024-05-12\n"
        b"Time: 08:30:15\n"
        b"Event: SystemCrash\n"
        b"Details:\n"
        b"Kernel panic - not syncing\n"
        b"Out of memory\n"
        b"=== LOG END ===\n"
    )
    data_size = len(data)

    payload = magic
    payload += struct.pack("<B", filename_len)
    payload += filename
    payload += struct.pack("<I", data_size)
    payload += data

    return payload, data

def test_server_response_and_extraction():
    payload, expected_data = create_bkp_payload()

    try:
        response = requests.post("http://127.0.0.1:8080/upload", data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect or send request to server on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    assert response.text.strip() == "SystemCrash", f"Expected response body 'SystemCrash', got '{response.text}'"

    # Check that zip slip was prevented
    hacked_log_path = "/home/user/hacked.log"
    assert not os.path.exists(hacked_log_path), "Zip Slip vulnerability detected: file was written outside the extracted directory!"

    # Check that file was extracted to the correct location with correct name
    extracted_file_path = "/home/user/extracted/20240512_083015_hacked.log"
    assert os.path.exists(extracted_file_path), f"Expected extracted file not found at {extracted_file_path}"

    # Check contents of the extracted file
    with open(extracted_file_path, "rb") as f:
        actual_data = f.read()

    assert actual_data == expected_data, "Extracted file contents do not match the original payload data"

def test_server_binary_exists():
    assert os.path.exists("/home/user/server"), "Server binary /home/user/server does not exist"
    assert os.access("/home/user/server", os.X_OK), "Server binary is not executable"