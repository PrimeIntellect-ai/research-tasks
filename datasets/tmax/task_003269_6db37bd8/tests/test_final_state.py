# test_final_state.py
import os
import json
import base64
import hmac
import hashlib
import subprocess
import time
import urllib.request
import urllib.error
import pytest

APP_DIR = "/home/user/app"
CONFIG_FILE = os.path.join(APP_DIR, "config.json")
SERVER_FILE = os.path.join(APP_DIR, "server.py")
SCANNER_FILE = os.path.join(APP_DIR, "scanner.py")
RESULTS_FILE = os.path.join(APP_DIR, "scan_results.json")

@pytest.fixture(scope="module")
def server_process():
    """Starts the Flask server in the background and ensures it is terminated after tests."""
    proc = subprocess.Popen(["python3", SERVER_FILE])

    # Wait for the server to be ready
    for _ in range(10):
        try:
            urllib.request.urlopen("http://localhost:5000/", timeout=1)
            break
        except urllib.error.URLError:
            time.sleep(0.5)
        except Exception:
            # If we get a 404 or other HTTP error, the server is at least responding
            break

    yield proc

    proc.terminate()
    proc.wait()

def test_config_updated():
    """Verify the config.json has the updated JWT_SECRET."""
    assert os.path.exists(CONFIG_FILE), f"{CONFIG_FILE} is missing."
    with open(CONFIG_FILE, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{CONFIG_FILE} is not valid JSON.")

    assert config.get("JWT_SECRET") == "r0tated_s3cr3t_999", "JWT_SECRET was not correctly updated to the new value."

def test_server_alg_none_rejected(server_process):
    """Verify that the server rejects 'alg=none' JWT tokens with a 401 Unauthorized."""
    header = base64.urlsafe_b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().rstrip('=')
    payload = base64.urlsafe_b64encode(json.dumps({"user": "admin"}).encode()).decode().rstrip('=')
    token = f"{header}.{payload}."

    req = urllib.request.Request('http://localhost:5000/api/data')
    req.add_header('Authorization', f'Bearer {token}')

    try:
        urllib.request.urlopen(req, timeout=5)
        pytest.fail("Server still accepts alg=none tokens (should return 401).")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401 Unauthorized for alg=none, got {e.code}."
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to server: {e}")

def test_server_valid_token_and_csp(server_process):
    """Verify that the server accepts valid tokens signed with the new secret and includes the CSP header."""
    secret = "r0tated_s3cr3t_999"
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip('=')
    payload = base64.urlsafe_b64encode(json.dumps({"user": "admin"}).encode()).decode().rstrip('=')
    sig = base64.urlsafe_b64encode(
        hmac.new(secret.encode(), (header + '.' + payload).encode(), hashlib.sha256).digest()
    ).decode().rstrip('=')
    token = f"{header}.{payload}.{sig}"

    req = urllib.request.Request('http://localhost:5000/api/data')
    req.add_header('Authorization', f'Bearer {token}')

    try:
        resp = urllib.request.urlopen(req, timeout=5)
        assert resp.status == 200, f"Server rejected valid token with new secret, got status {resp.status}."

        expected_csp = "default-src 'self'; script-src 'self' 'nonce-random123';"
        actual_csp = resp.headers.get('Content-Security-Policy')
        assert actual_csp == expected_csp, f"CSP header is missing or incorrect. Expected: {expected_csp}, Got: {actual_csp}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Server rejected valid token, got HTTP Error {e.code}.")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to server: {e}")

def test_scanner_script(server_process):
    """Verify that the scanner script runs successfully and produces the correct output."""
    assert os.path.exists(SCANNER_FILE), f"{SCANNER_FILE} does not exist."

    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)

    result = subprocess.run(["python3", SCANNER_FILE], capture_output=True, text=True)
    assert result.returncode == 0, f"Scanner script failed to execute. Stderr: {result.stderr}"

    assert os.path.exists(RESULTS_FILE), f"{RESULTS_FILE} was not created by the scanner."

    with open(RESULTS_FILE, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_FILE} is not valid JSON.")

    assert results.get("alg_none_rejected") is True, "'alg_none_rejected' in scan results should be True."
    assert results.get("csp_enforced") is True, "'csp_enforced' in scan results should be True."