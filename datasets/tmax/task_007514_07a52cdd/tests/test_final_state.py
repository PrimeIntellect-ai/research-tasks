# test_final_state.py
import os
import struct
import pytest

ORGANIZED_DIR = "/home/user/organized_projects"
LOG_FILE = "/home/user/migration.log"

EXPECTED_FILES = {
    "report_2020.txt": b'Report data for 2020',
    "logo_v2.png": b'\x89PNG\r\n\x1a\n\x00\x00',
    "config.ini": b'[settings]\nkey=value',
}

EXPECTED_LOG_LINES = [
    "file_001.dat -> report_2020.txt [V1_UPGRADED]",
    "file_002.dat -> logo_v2.png [V2_UNCHANGED]",
    "file_003.dat -> config.ini [V1_UPGRADED]",
]

def test_migration_log_exists_and_content():
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} is not a file."

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == EXPECTED_LOG_LINES, f"Log file contents do not match expected output. Got: {lines}"

def test_organized_directory_exists():
    assert os.path.exists(ORGANIZED_DIR), f"Directory {ORGANIZED_DIR} does not exist."
    assert os.path.isdir(ORGANIZED_DIR), f"{ORGANIZED_DIR} is not a directory."

@pytest.mark.parametrize("filename,payload", EXPECTED_FILES.items())
def test_organized_files(filename, payload):
    file_path = os.path.join(ORGANIZED_DIR, filename)
    assert os.path.exists(file_path), f"Expected organized file {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "rb") as f:
        data = f.read()

    assert len(data) >= 7, f"File {filename} is too short to contain a valid header."

    # Check Magic Number
    assert data[:4] == b'LEGA', f"Incorrect magic number in {filename}. Expected b'LEGA'."

    # Check Version
    assert data[4:5] == b'\x02', f"Incorrect version in {filename}. Expected 0x02 for V2."

    # Check Filename Length
    name_len = struct.unpack('<H', data[5:7])[0]
    expected_filename_bytes = filename.encode('utf-16le')
    expected_name_len = len(expected_filename_bytes)

    assert name_len == expected_name_len, f"Incorrect filename length in {filename}. Expected {expected_name_len}, got {name_len}."

    # Check Filename Bytes
    actual_filename_bytes = data[7:7+name_len]
    assert actual_filename_bytes == expected_filename_bytes, f"Incorrect filename encoding in {filename}. Expected {expected_filename_bytes}, got {actual_filename_bytes}."

    # Check Payload
    actual_payload = data[7+name_len:]
    assert actual_payload == payload, f"Incorrect payload in {filename}. Expected {payload}, got {actual_payload}."