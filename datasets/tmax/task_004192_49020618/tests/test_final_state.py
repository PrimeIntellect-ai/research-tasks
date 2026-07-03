# test_final_state.py
import pytest
import requests
import urllib.parse

def compute_expected_hash(text: str) -> int:
    return sum(b * (i + 1) for i, b in enumerate(text.encode('utf-8'))) % 1000003

@pytest.mark.parametrize("text", [
    "hello",
    "test with spaces",
    "complex UTF-8: 🚀 ëñçödîñg",
    "a",
    "12345",
    "A very long string with multiple characters to test the modulo arithmetic correctly!"
])
def test_compute_endpoint(text):
    encoded_text = urllib.parse.quote(text)
    url = f"http://127.0.0.1:8080/compute?text={encoded_text}"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or retrieve data at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response: {response.text}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type to include 'application/json', got '{content_type}'"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert "hash" in data, f"Response JSON does not contain the required 'hash' key. Got: {data}"

    expected_hash = compute_expected_hash(text)
    assert data["hash"] == expected_hash, f"For text '{text}', expected hash {expected_hash}, got {data['hash']}"