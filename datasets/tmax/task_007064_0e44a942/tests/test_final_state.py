# test_final_state.py
import os
import urllib.request
import urllib.error

def test_new_creds_file():
    filepath = '/home/user/new_creds.txt'
    assert os.path.isfile(filepath), f"{filepath} does not exist."
    with open(filepath, 'r') as f:
        content = f.read().strip()
    assert content == "CSP_SECURE_PASSWORD_99", f"Expected 'CSP_SECURE_PASSWORD_99' in {filepath}, got '{content}'"

def test_csp_proxy_script_exists():
    filepath = '/home/user/csp_proxy.py'
    assert os.path.isfile(filepath), f"{filepath} does not exist."

def test_proxy_running_and_injects_csp():
    req = urllib.request.Request("http://127.0.0.1:8080/rotate_creds", method="POST")
    try:
        response = urllib.request.urlopen(req, timeout=5)
        headers = response.headers
        body = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        headers = e.headers
        body = e.read().decode('utf-8')
    except Exception as e:
        raise AssertionError(f"Failed to connect to proxy on port 8080: {e}")

    # Check for CSP header
    csp_header = headers.get('Content-Security-Policy')
    assert csp_header is not None, "Content-Security-Policy header is missing from proxy response."

    expected_csp = "default-src 'none'; frame-ancestors 'none';"
    assert csp_header.strip() == expected_csp, f"Expected CSP header '{expected_csp}', got '{csp_header}'"

    # Check that the proxy actually forwarded to the Flask app
    # The Flask app returns {"error": "Missing token"} for a POST without auth
    assert "error" in body or "Missing token" in body, "Proxy did not forward the response from the legacy service correctly."