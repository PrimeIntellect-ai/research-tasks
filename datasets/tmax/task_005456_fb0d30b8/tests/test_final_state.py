# test_final_state.py
import os
import socket
import ssl
import pytest

def test_certs_exist():
    """Verify that the TLS certificates were generated in the correct location."""
    cert_path = '/home/user/certs/server.crt'
    key_path = '/home/user/certs/server.key'

    assert os.path.isfile(cert_path), f"Certificate not found at {cert_path}"
    assert os.path.isfile(key_path), f"Private key not found at {key_path}"

def test_script_exists_and_executable():
    """Verify that the upload server script exists and is executable."""
    script_path = '/home/user/upload_server.sh'
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def send_https_request(path, token):
    """Helper to send a raw HTTPS request and return the response text."""
    context = ssl._create_unverified_context()
    try:
        with socket.create_connection(('127.0.0.1', 8443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname='127.0.0.1') as ssock:
                request = (
                    f"POST {path} HTTP/1.1\r\n"
                    f"Host: 127.0.0.1:8443\r\n"
                    f"X-Auth-Token: {token}\r\n"
                    f"Connection: close\r\n\r\n"
                )
                ssock.sendall(request.encode('utf-8'))

                response = b""
                while True:
                    try:
                        chunk = ssock.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                    except socket.timeout:
                        break
                return response.decode('utf-8', errors='ignore')
    except ConnectionRefusedError:
        pytest.fail("Connection refused. Is the server running on 127.0.0.1:8443?")
    except ssl.SSLError as e:
        pytest.fail(f"SSL error occurred, TLS might not be configured correctly: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error connecting to server: {e}")

def test_valid_request():
    """Test that a valid request with the correct token and safe filename succeeds."""
    response = send_https_request('/upload?file=data.txt', 'SecOps-99A2-XYZ')
    assert "200 OK" in response, f"Expected '200 OK' in response, got:\n{response}"
    assert "Success" in response, f"Expected 'Success' in response body, got:\n{response}"

def test_invalid_token():
    """Test that a request with an invalid token is rejected with 401 Unauthorized."""
    response = send_https_request('/upload?file=data.txt', 'WrongToken')
    assert "401 Unauthorized" in response, f"Expected '401 Unauthorized' in response, got:\n{response}"

def test_path_traversal_attempt():
    """Test that a request attempting path traversal (../) is rejected with 403 Forbidden."""
    response = send_https_request('/upload?file=../../../etc/shadow', 'SecOps-99A2-XYZ')
    assert "403 Forbidden" in response, f"Expected '403 Forbidden' in response, got:\n{response}"

def test_absolute_path_attempt():
    """Test that a request using an absolute path is rejected with 403 Forbidden."""
    response = send_https_request('/upload?file=/etc/passwd', 'SecOps-99A2-XYZ')
    assert "403 Forbidden" in response, f"Expected '403 Forbidden' in response, got:\n{response}"