# test_final_state.py

import os
import json
import urllib.request
import pytest

def test_shared_library_compiled():
    """Verify that the shared library was compiled."""
    lib_path = "/home/user/lib/libchecksum.so"
    assert os.path.isfile(lib_path), f"Shared library not found at {lib_path}. Did you compile checksum.c?"

def test_server_ready_file_exists():
    """Verify that the server_ready.txt file was created."""
    ready_file = "/home/user/server_ready.txt"
    assert os.path.isfile(ready_file), f"Ready flag file not found at {ready_file}. Ensure the server is started and the file is created."

def test_api_endpoint_response():
    """Verify the REST API endpoint returns the correct schema and checksum."""
    url = "http://127.0.0.1:8080/schema/v2"

    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}"
            body = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect to the API or read response: {e}")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail("API response is not valid JSON.")

    assert "checksum" in data, "Response JSON is missing the 'checksum' key."
    assert "data" in data, "Response JSON is missing the 'data' key."

    # Verify checksum
    assert data["checksum"] == 48, f"Incorrect checksum. Expected 48, got {data['checksum']}."

    # Verify migrated schema
    schema_data = data["data"]
    assert isinstance(schema_data, dict), "The 'data' field should be a JSON object."

    assert "account_holders" in schema_data, "Missing 'account_holders' in migrated schema."
    assert "users" not in schema_data, "The 'users' key was not renamed/removed."

    assert "version" in schema_data, "Missing 'version' in migrated schema."
    assert schema_data["version"] == 2, f"Expected version 2, got {schema_data['version']}."

    assert "legacy_flag" not in schema_data, "The 'legacy_flag' was not removed from the schema."

    assert "environment" in schema_data, "Missing 'environment' in migrated schema."
    assert schema_data["environment"] == "production", f"Expected environment 'production', got {schema_data['environment']}."

    assert len(schema_data["account_holders"]) == 2, "Incorrect number of account_holders."