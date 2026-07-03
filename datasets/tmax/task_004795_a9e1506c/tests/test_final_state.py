# test_final_state.py

import os
import socket
import sqlite3
import pytest

def mask_string(s: str) -> str:
    """Python implementation of the masking algorithm."""
    reversed_s = s[::-1]
    return "".join(f"{ord(c) ^ 0x42:02x}" for c in reversed_s)

def test_tcp_service_and_database():
    """Test the TCP service protocol and database insertion."""
    host = "127.0.0.1"
    port = 9090
    db_path = "/home/user/anonymized.db"

    # Prepare test data
    csv_data = [
        "100,Charlie,charlie@test.com,123-45-6789",
        "101,Dave,dave@example.net,987-65-4321"
    ]

    payload = "BULK_LOAD\n"
    for line in csv_data:
        payload += line + "\n"
    payload += "EOF\n"

    # Connect to the service
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            sock.sendall(payload.encode('utf-8'))

            # Read response
            response = sock.recv(1024).decode('utf-8')
            assert response == "SUCCESS 2\n", f"Expected 'SUCCESS 2\\n', got {repr(response)}"
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {host}:{port}. Is the service running?")
    except socket.timeout:
        pytest.fail(f"Connection timed out when communicating with {host}:{port}.")

    # Check the database
    assert os.path.exists(db_path), f"Database file not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check schema
    cursor.execute("PRAGMA table_info(users);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}
    assert "id" in columns, "Column 'id' missing from users table"
    assert "name" in columns, "Column 'name' missing from users table"
    assert "email" in columns, "Column 'email' missing from users table"
    assert "ssn" in columns, "Column 'ssn' missing from users table"

    # Check data
    cursor.execute("SELECT id, name, email, ssn FROM users WHERE id IN (100, 101) ORDER BY id;")
    rows = cursor.fetchall()
    assert len(rows) == 2, f"Expected 2 rows in DB, got {len(rows)}"

    # Validate row 100
    assert rows[0][0] == 100
    assert rows[0][1] == "Charlie"
    assert rows[0][2] == mask_string("charlie@test.com"), f"Email for id 100 is incorrectly masked"
    assert rows[0][3] == mask_string("123-45-6789"), f"SSN for id 100 is incorrectly masked"

    # Validate row 101
    assert rows[1][0] == 101
    assert rows[1][1] == "Dave"
    assert rows[1][2] == mask_string("dave@example.net"), f"Email for id 101 is incorrectly masked"
    assert rows[1][3] == mask_string("987-65-4321"), f"SSN for id 101 is incorrectly masked"

    conn.close()