import os
import requests
import xml.etree.ElementTree as ET
import pytest

def test_pii_masker_fixed():
    """Test that the /app/pii-masker/masker.go file has been fixed."""
    masker_path = "/app/pii-masker/masker.go"
    assert os.path.isfile(masker_path), f"The file {masker_path} does not exist."

    with open(masker_path, "r") as f:
        content = f.read()

    assert '"strings"' in content or "\n\tstrings\n" in content or "strings" in content, "The file masker.go is still missing the 'strings' import."

def test_server_unauthorized():
    """Test that the server rejects requests without the correct Authorization header."""
    url = "http://127.0.0.1:8080/process"
    payload = {
        "batch_id": "test-1",
        "items": [{"id": 1, "content": "Email test@example.com"}]
    }

    # Missing Auth
    try:
        resp = requests.post(url, json=payload, timeout=2)
        assert resp.status_code == 401, f"Expected HTTP 401 for missing auth, got {resp.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:8080. Is it running?")

    # Incorrect Auth
    headers = {"Authorization": "Token wrong-secret"}
    resp = requests.post(url, json=payload, headers=headers, timeout=2)
    assert resp.status_code == 401, f"Expected HTTP 401 for incorrect auth, got {resp.status_code}"

def test_server_process_success():
    """Test that the server processes requests correctly and returns the expected XML."""
    url = "http://127.0.0.1:8080/process"
    headers = {"Authorization": "Token v1-automation-secret"}
    payload = {
        "batch_id": "B-992",
        "items": [
            {"id": 1, "content": "Contact me at john.doe@example.com immediately."},
            {"id": 2, "content": "My phone is 555-0199."}
        ]
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:8080. Is it running?")

    assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}. Response: {resp.text}"
    assert "application/xml" in resp.headers.get("Content-Type", ""), f"Expected Content-Type: application/xml, got {resp.headers.get('Content-Type')}"

    # Parse XML
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        pytest.fail(f"Failed to parse XML response: {e}. Response body: {resp.text}")

    assert root.tag == "BatchResponse", f"Expected root tag 'BatchResponse', got '{root.tag}'"

    batch_id = root.find("BatchID")
    assert batch_id is not None, "Missing 'BatchID' element in XML response"
    assert batch_id.text == "B-992", f"Expected BatchID 'B-992', got '{batch_id.text}'"

    items_el = root.find("Items")
    assert items_el is not None, "Missing 'Items' element in XML response"

    items = items_el.findall("Item")
    assert len(items) == 2, f"Expected 2 items in XML response, got {len(items)}"

    # Create a map to check results regardless of ordering (parallel processing might change order)
    results = {}
    for item in items:
        id_el = item.find("ID")
        content_el = item.find("MaskedContent")
        assert id_el is not None, "Missing 'ID' element in Item"
        assert content_el is not None, "Missing 'MaskedContent' element in Item"
        results[id_el.text] = content_el.text

    assert "1" in results, "Item with ID 1 missing from response"
    assert "2" in results, "Item with ID 2 missing from response"

    assert results["1"] == "Contact me at [REDACTED_EMAIL] immediately.", f"Incorrect masked content for ID 1: {results['1']}"
    assert results["2"] == "My phone is 555-0199.", f"Incorrect masked content for ID 2: {results['2']}"