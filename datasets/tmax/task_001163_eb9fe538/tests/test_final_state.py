# test_final_state.py

import os
import pytest
import requests

def test_makefile_fixed():
    """Verify that the Makefile has been updated to include OpenSSL flags."""
    makefile_path = '/app/policy-daemon/Makefile'
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing"

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert '-lssl' in content or 'MG_ENABLE_OPENSSL' in content or '-lcrypto' in content, \
        "Makefile does not appear to contain the required OpenSSL compilation flags (-lssl, -lcrypto, or -D MG_ENABLE_OPENSSL=1)."

def test_certs_exist():
    """Verify that the TLS certificates have been generated in the correct location."""
    crt_path = '/app/policy-daemon/certs/server.crt'
    key_path = '/app/policy-daemon/certs/server.key'

    assert os.path.isfile(crt_path), f"Certificate file {crt_path} is missing"
    assert os.path.isfile(key_path), f"Key file {key_path} is missing"

def test_server_c_fixed():
    """Verify that the C code has been patched to exit on privilege drop failure."""
    server_c_path = '/app/policy-daemon/server.c'
    assert os.path.isfile(server_c_path), f"{server_c_path} is missing"

    with open(server_c_path, 'r') as f:
        content = f.read()

    # The student was instructed to add exit(1);
    # We check for a generic exit or return to be flexible but verify the fix intent.
    assert 'exit(' in content or 'return ' in content.split('drop_privileges_and_init() < 0')[1], \
        "server.c does not seem to exit or return when drop_privileges_and_init() fails."

def test_log_file_exists():
    """Verify that the completion log file exists and contains 'DONE'."""
    log_path = '/home/user/task_complete.log'
    assert os.path.isfile(log_path), f"Log file {log_path} is missing"

    with open(log_path, 'r') as f:
        content = f.read()

    assert 'DONE' in content, f"Log file {log_path} does not contain the word 'DONE'"

def test_service_running():
    """Verify that the policy-daemon is running, accessible over HTTPS, and enforces policy."""
    url = 'https://localhost:8443/api/policy'
    headers = {"Authorization": "Bearer devsecops-token-99"}

    # We disable SSL verification (verify=False) because it's a self-signed cert
    # and we just want to verify the service is up and serving the correct content.
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the policy-daemon service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert data.get("status") == "policy_enforced", f"Expected status 'policy_enforced', got {data.get('status')}"
    assert data.get("version") == "1.0", f"Expected version '1.0', got {data.get('version')}"

def test_service_unauthorized():
    """Verify that the policy-daemon rejects unauthorized requests."""
    url = 'https://localhost:8443/api/policy'
    headers = {"Authorization": "Bearer invalid-token"}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the policy-daemon service at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for bad token, got {response.status_code}"