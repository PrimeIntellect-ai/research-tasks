# test_final_state.py

import os
import requests
import pytest

def test_required_files_exist():
    """Verify that the student created the required scripts."""
    secure_upload_path = "/home/user/secure_upload.py"
    firewall_script_path = "/home/user/firewall_setup.sh"

    assert os.path.exists(secure_upload_path), f"Missing required file: {secure_upload_path}"
    assert os.path.exists(firewall_script_path), f"Missing required file: {firewall_script_path}"

def test_incident_report_content():
    """Verify the incident report contains the cracked password and backdoor port."""
    report_path = "/home/user/incident_report.log"
    assert os.path.exists(report_path), f"Missing required file: {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "Incident report does not contain enough lines."
    assert lines[0] == "butterfly", f"Expected first line to be 'butterfly', got '{lines[0]}'"
    assert lines[1] == "1337", f"Expected second line to be '1337', got '{lines[1]}'"

def test_service_csp_header():
    """Verify the Python service is running and returns the correct CSP header."""
    url = "http://127.0.0.1:8080/"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the secure upload service at {url}: {e}")

    csp_header = response.headers.get("Content-Security-Policy")
    assert csp_header is not None, "Content-Security-Policy header is missing from the response."
    assert csp_header == "default-src 'self'", f"Incorrect CSP header value. Expected \"default-src 'self'\", got \"{csp_header}\""

def test_service_path_traversal_protection():
    """Verify the Python service rejects or sanitizes path traversal attempts in file uploads."""
    url = "http://127.0.0.1:8080/upload"
    malicious_filename = "../../../etc/passwd"
    files = {"file": (malicious_filename, b"test content")}

    try:
        response = requests.post(url, files=files, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the secure upload service at {url}: {e}")

    # The service should either reject the request (e.g., 400 Bad Request) or accept it safely (200 OK)
    # but it must not crash (500 Internal Server Error)
    assert response.status_code in [200, 201, 400, 403], f"Unexpected status code {response.status_code} when attempting path traversal."

    # If it accepted the file, ensure the malicious path is not reflected verbatim in a success message
    if response.status_code in [200, 201]:
        assert malicious_filename not in response.text, "Service accepted the upload but appears to have reflected the unsanitized malicious path."