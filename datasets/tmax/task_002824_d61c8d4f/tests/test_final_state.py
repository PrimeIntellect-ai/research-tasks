# test_final_state.py
import os
import stat
import subprocess
import tempfile
import pytest
import requests

PROXY_URL = "http://127.0.0.1:9090/exploit"
FLAG_PATH = "/home/user/flag.txt"
LOOT_PATH = "/home/user/loot.txt"
CA_CERT_PATH = "/home/user/ca.pem"
CA_KEY_PATH = "/home/user/ca.key"  # Assuming the test harness leaves the key here or in the pem

@pytest.fixture(scope="session")
def flag_content():
    with open(FLAG_PATH, "r") as f:
        return f.read().strip()

@pytest.fixture(scope="session")
def valid_cert():
    """Generates a valid client certificate signed by the local CA for testing."""
    # If the CA key is bundled in the PEM or exists alongside it
    ca_key = CA_KEY_PATH if os.path.exists(CA_KEY_PATH) else CA_CERT_PATH

    with tempfile.TemporaryDirectory() as tmpdir:
        client_key = os.path.join(tmpdir, "client.key")
        client_csr = os.path.join(tmpdir, "client.csr")
        client_crt = os.path.join(tmpdir, "client.crt")

        # Generate client key and CSR
        subprocess.run(["openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes", 
                        "-keyout", client_key, "-out", client_csr, "-subj", "/CN=client"], 
                       check=True, capture_output=True)

        # Sign with CA
        subprocess.run(["openssl", "x509", "-req", "-in", client_csr, "-CA", CA_CERT_PATH, 
                        "-CAkey", ca_key, "-CAcreateserial", "-out", client_crt, "-days", "1"], 
                       check=True, capture_output=True)

        with open(client_crt, "r") as f:
            return f.read()

@pytest.fixture(scope="session")
def invalid_cert():
    """Generates an invalid, self-signed client certificate."""
    with tempfile.TemporaryDirectory() as tmpdir:
        invalid_crt = os.path.join(tmpdir, "invalid.crt")
        subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", 
                        "-keyout", os.path.join(tmpdir, "invalid.key"), "-out", invalid_crt, 
                        "-days", "1", "-subj", "/CN=invalid"], 
                       check=True, capture_output=True)
        with open(invalid_crt, "r") as f:
            return f.read()

def test_proxy_invalid_auth(valid_cert):
    """Test that the proxy rejects requests with an invalid X-Proxy-Auth header."""
    headers = {"X-Proxy-Auth": "Wrong-Auth"}
    try:
        response = requests.post(PROXY_URL, headers=headers, data=valid_cert, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {PROXY_URL}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 for invalid auth, got {response.status_code}. Response: {response.text}"

def test_proxy_invalid_cert(invalid_cert):
    """Test that the proxy rejects requests with an invalid certificate."""
    headers = {"X-Proxy-Auth": "RedTeamOps-2024"}
    try:
        response = requests.post(PROXY_URL, headers=headers, data=invalid_cert, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {PROXY_URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid cert, got {response.status_code}. Response: {response.text}"

def test_proxy_successful_exploit(valid_cert, flag_content):
    """Test that the proxy successfully exploits the target and returns the flag."""
    # Ensure loot file doesn't exist before successful run (cleanup if necessary)
    if os.path.exists(LOOT_PATH):
        os.chmod(LOOT_PATH, 0o600)
        os.remove(LOOT_PATH)

    headers = {"X-Proxy-Auth": "RedTeamOps-2024"}
    try:
        response = requests.post(PROXY_URL, headers=headers, data=valid_cert, timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {PROXY_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for successful exploit, got {response.status_code}. Response: {response.text}"
    assert flag_content in response.text, f"Expected flag '{flag_content}' in response, got: {response.text}"

def test_loot_file_created_and_permissions(flag_content):
    """Test that the loot file was created with the correct content and permissions."""
    assert os.path.exists(LOOT_PATH), f"Loot file {LOOT_PATH} was not created."

    with open(LOOT_PATH, "r") as f:
        loot_content = f.read().strip()

    assert flag_content in loot_content, f"Loot file does not contain the correct flag. Expected '{flag_content}', got '{loot_content}'"

    file_stat = os.stat(LOOT_PATH)
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o400, f"Expected permissions 0400 for {LOOT_PATH}, got {oct(permissions)}"