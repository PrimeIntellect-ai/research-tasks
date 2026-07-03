# test_final_state.py

import os
import socket
import json
import re
import pytest

def test_cjson_fixed_and_built():
    """Verify that the cJSON Makefile was fixed and the library was built."""
    makefile_path = "/app/cJSON-1.7.15/Makefile"
    assert os.path.exists(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        makefile_content = f.read()

    assert "CC = gcc\n" in makefile_content or "CC=gcc\n" in makefile_content or "CC = gcc" in makefile_content, "The Makefile was not fixed to use 'gcc'."
    assert "gccc" not in makefile_content, "The 'gccc' typo is still present in the Makefile."

    # Check that the library was built
    lib_exists = os.path.exists("/app/cJSON-1.7.15/libcjson.so") or \
                 os.path.exists("/app/cJSON-1.7.15/libcjson.so.1.7.15") or \
                 os.path.exists("/app/cJSON-1.7.15/libcjson.a")
    assert lib_exists, "The cJSON library (libcjson.so or libcjson.a) was not built in /app/cJSON-1.7.15."

def send_tcp_request(host, port, message, timeout=5.0):
    """Helper to send a TCP request and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            s.sendall(message.encode('utf-8'))

            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
            return response.decode('utf-8')
        except ConnectionRefusedError:
            pytest.fail(f"Connection refused on {host}:{port}. Is the service running?")
        except socket.timeout:
            pytest.fail(f"Connection timed out on {host}:{port}.")

def test_service_invalid_command():
    """Verify that the service returns ERROR\\n for invalid commands."""
    response = send_tcp_request("127.0.0.1", 8000, "BAD_COMMAND\n")
    assert response == "ERROR\n", f"Expected 'ERROR\\n' for invalid command, got {repr(response)}"

def test_service_valid_command_and_masking():
    """Verify that the service returns correctly masked JSON data for a valid command."""
    response = send_tcp_request("127.0.0.1", 8000, "RUN_ETL SECRET_TOKEN_42\n")

    # Check the ending
    assert response.endswith("\nEND\n"), f"Response must end with '\\nEND\\n', got {repr(response[-10:])}"

    # Extract the JSON part
    json_str = response[:-5] # remove "\nEND\n"

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON payload: {e}. Payload was: {repr(json_str)}")

    assert isinstance(data, list), "Expected a JSON array of objects."
    assert len(data) == 2, f"Expected 2 records, got {len(data)}."

    # Expected masked data based on initial setup
    expected_data = {
        1: {"name": "Alice Smith", "email": "a***@example.com", "credit_card": "XXXXXXXXXXXX5678"},
        2: {"name": "Bob Jones", "email": "b***@test.org", "credit_card": "XXXXXXXXXXXX5432"}
    }

    for record in data:
        assert "id" in record, "Record missing 'id' field."
        assert "name" in record, "Record missing 'name' field."
        assert "email" in record, "Record missing 'email' field."
        assert "credit_card" in record, "Record missing 'credit_card' field."

        record_id = record["id"]
        assert record_id in expected_data, f"Unexpected record ID {record_id}."

        expected = expected_data[record_id]
        assert record["name"] == expected["name"], f"Name mismatch for ID {record_id}."

        # Verify exact masking rules
        assert re.match(r"^.\*\*\*@[^@]+$", record["email"]), f"Email masking failed for ID {record_id}: {record['email']}"
        assert record["email"] == expected["email"], f"Email mismatch for ID {record_id}."

        assert re.match(r"^X{12}\d{4}$", record["credit_card"]), f"Credit card masking failed for ID {record_id}: {record['credit_card']}"
        assert record["credit_card"] == expected["credit_card"], f"Credit card mismatch for ID {record_id}."