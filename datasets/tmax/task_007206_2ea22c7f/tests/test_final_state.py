# test_final_state.py
import os

RESPONSE_FILE = "/home/user/response.txt"

def test_response_file_exists():
    """Check that the response.txt file was created."""
    assert os.path.isfile(RESPONSE_FILE), (
        f"Expected output file {RESPONSE_FILE} does not exist. "
        "Did you execute the exploit and redirect the output to this file?"
    )

def test_response_status_200():
    """Check that the response indicates a successful token bypass (200 OK)."""
    with open(RESPONSE_FILE, "rb") as f:
        content = f.read()

    assert content.startswith(b"HTTP/1.1 200 OK"), (
        "The response does not start with 'HTTP/1.1 200 OK'. "
        "The token calculation may be incorrect, or the daemon rejected the request."
    )

def test_crlf_xss_injection():
    """Check that the XSS payload was successfully injected into the response body via CRLF."""
    with open(RESPONSE_FILE, "rb") as f:
        content = f.read()

    # Split by the first double CRLF to separate the HTTP headers from the body
    parts = content.split(b"\r\n\r\n", 1)
    assert len(parts) == 2, (
        "Could not find a double CRLF (\\r\\n\\r\\n) separating headers and body in the response. "
        "The CRLF injection may have failed."
    )

    body = parts[1]
    expected_payload = b"<svg onload=alert(document.cookie)>"

    assert expected_payload in body, (
        "The expected XSS payload was not found strictly in the response body. "
        "Ensure the payload is injected after the CRLF sequence to bypass the CSP header. "
        f"Actual body content found: {body!r}"
    )