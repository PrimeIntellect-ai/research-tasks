# test_final_state.py

import os
import requests
import pytest

def test_go_humanize_fixed():
    """Test that the syntax error in times.go has been fixed."""
    times_go_path = "/app/go-humanize/times.go"
    assert os.path.isfile(times_go_path), f"File missing: {times_go_path}"
    with open(times_go_path, "r") as f:
        content = f.read()
    # The syntax error was a missing closing quote. We should check if it's fixed.
    assert 'return "just now"' in content, "The syntax error in times.go does not appear to be fixed."

def test_wide_events_tsv_content():
    """Test that wide_events.tsv is correctly formatted and contains the right data."""
    tsv_path = "/home/user/processed/wide_events.tsv"
    assert os.path.isfile(tsv_path), f"File missing: {tsv_path}"

    with open(tsv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "TSV file should contain at least a header and one data row."

    header = lines[0].split("\t")
    expected_header = ["timestamp", "event_id", "en", "es", "fr", "zh"]
    assert header == expected_header, f"TSV header is incorrect. Expected {expected_header}, got {header}"

    # Check the specific row from the initial setup
    found_row = False
    for line in lines[1:]:
        cols = line.split("\t")
        if len(cols) == 6 and cols[1] == "EVT-001":
            assert cols[0] == "2023-10-01T10:00:00Z", "Incorrect timestamp for EVT-001"
            assert cols[2] == "Hello", "Incorrect 'en' translation"
            assert cols[3] == "Hola", "Incorrect 'es' translation"
            assert cols[4] == "Bonjour", "Incorrect 'fr' translation"
            assert cols[5] == "MISSING", "Incorrect 'zh' translation, should be MISSING"
            found_row = True
            break

    assert found_row, "The expected row for EVT-001 was not found in the TSV."

def test_server_valid_request():
    """Test that the server responds correctly to a valid request with Auth header."""
    url = "http://127.0.0.1:8080/timeline?event_id=EVT-001&lang=es"
    headers = {"Authorization": "Bearer loc-eng-token"}

    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    text = response.text
    assert "Event EVT-001 occurred at" in text, "Response missing expected event ID text."
    assert "Translation: Hola" in text, "Response missing expected translation text."
    assert "ago" in text, "Response missing humanized time text."

def test_server_unauthorized_request():
    """Test that the server rejects requests without the Auth header."""
    url = "http://127.0.0.1:8080/timeline?event_id=EVT-001&lang=es"

    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code in [401, 403], f"Expected status code 401 or 403 for unauthorized request, got {response.status_code}."

def test_server_missing_translation():
    """Test that the server returns 404 for a missing translation."""
    url = "http://127.0.0.1:8080/timeline?event_id=EVT-001&lang=zh"
    headers = {"Authorization": "Bearer loc-eng-token"}

    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 404, f"Expected status code 404 for missing translation, got {response.status_code}."

def test_server_missing_event():
    """Test that the server returns 404 for a missing event."""
    url = "http://127.0.0.1:8080/timeline?event_id=EVT-999&lang=en"
    headers = {"Authorization": "Bearer loc-eng-token"}

    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 404, f"Expected status code 404 for missing event, got {response.status_code}."