# test_final_state.py

import os
import socket
import struct
import json
import zlib
import sqlite3
import time
import pytest

DB_PATH = "/home/user/telemetry.db"
HOST = "127.0.0.1"
PORT = 9999

def compute_checksum(payload: bytes) -> int:
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    return crc ^ 0x87654321

def create_packet(payload_dict: dict, valid_checksum: bool = True) -> bytes:
    payload_bytes = json.dumps(payload_dict).encode('utf-8')
    length = len(payload_bytes)

    if valid_checksum:
        checksum = compute_checksum(payload_bytes)
    else:
        checksum = compute_checksum(payload_bytes) ^ 0xFFFFFFFF # Invalid

    return struct.pack('<II', length, checksum) + payload_bytes

def test_db_migration():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings_v2';")
    assert cursor.fetchone() is not None, "Table 'readings_v2' was not created."

    cursor.execute("PRAGMA table_info(readings_v2);")
    columns = {row[1] for row in cursor.fetchall()}
    expected_columns = {'id', 'device_id', 'temperature'}
    assert expected_columns.issubset(columns), f"Expected columns {expected_columns}, found {columns}"

    cursor.execute("SELECT id, device_id, temperature FROM readings_v2 WHERE id=1;")
    row = cursor.fetchone()
    assert row is not None, "Migrated row with id=1 not found in 'readings_v2'."
    assert row == (1, 100, 42.5), f"Migrated row incorrect: {row}"

    conn.close()

def test_tcp_server_valid_packet():
    # Send a valid packet
    payload = {"device": 999, "temp": 123.45}
    packet = create_packet(payload, valid_checksum=True)

    try:
        with socket.create_connection((HOST, PORT), timeout=2) as s:
            s.sendall(packet)
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to {HOST}:{PORT}. Is the server running?")

    # Give the server a moment to process and insert
    time.sleep(0.5)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT device_id, temperature FROM readings_v2 WHERE device_id=999;")
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "Valid packet was not inserted into the database."
    assert row == (999, 123.45), f"Inserted data incorrect: {row}"

def test_tcp_server_invalid_packet():
    # Send an invalid packet
    payload = {"device": 888, "temp": 54.32}
    packet = create_packet(payload, valid_checksum=False)

    try:
        with socket.create_connection((HOST, PORT), timeout=2) as s:
            s.sendall(packet)
            # The server should drop the connection. If we try to read, it should return empty (EOF)
            # or throw an error if we try to send more data.
            try:
                response = s.recv(1024)
                assert not response, "Expected connection to be dropped, but received data."
            except (ConnectionResetError, BrokenPipeError):
                pass # Expected
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to {HOST}:{PORT}. Is the server running?")

    time.sleep(0.5)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT device_id FROM readings_v2 WHERE device_id=888;")
    row = cursor.fetchone()
    conn.close()

    assert row is None, "Invalid packet was incorrectly inserted into the database."