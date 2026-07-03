# test_final_state.py
import base64
import html
import json
import requests
import pytest

def encode_payload(text: str) -> str:
    # Shift +3 to simulate the input that will be unshifted (-3) by the service
    shifted = bytes((b + 3) % 256 for b in text.encode('utf-8'))
    return base64.b64encode(shifted).decode('utf-8')

def test_service_processing():
    url = "http://127.0.0.1:8080/process"

    test_cases = [
        "Normal log entry without special chars",
        "<script>alert(\"XSS & 'injection'\")</script>",
        "Another test < > & \" '"
    ]

    for original_text in test_cases:
        payload = encode_payload(original_text)

        try:
            response = requests.post(url, json={"payload": payload}, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the service at {url}: {e}")

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        try:
            resp_json = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "status" in resp_json, "Response JSON missing 'status' key"
        assert resp_json["status"] == "success", f"Expected status 'success', got {resp_json['status']}"
        assert "safe_log" in resp_json, "Response JSON missing 'safe_log' key"

        # Calculate expected safe log
        # The service should replace &, <, >, ", '
        expected_safe_log = original_text.replace("&", "&amp;") \
                                         .replace("<", "&lt;") \
                                         .replace(">", "&gt;") \
                                         .replace("\"", "&quot;") \
                                         .replace("'", "&#x27;")

        # Python's html.escape might use &#x27; for single quote, accept both &#x27; and &#39;
        alt_expected_safe_log = original_text.replace("&", "&amp;") \
                                             .replace("<", "&lt;") \
                                             .replace(">", "&gt;") \
                                             .replace("\"", "&quot;") \
                                             .replace("'", "&#39;")

        actual_safe_log = resp_json["safe_log"]
        assert actual_safe_log in (expected_safe_log, alt_expected_safe_log), \
            f"Sanitization failed. Expected '{expected_safe_log}' or '{alt_expected_safe_log}', got '{actual_safe_log}'"