# test_final_state.py
import os
import stat
import subprocess
import requests
import time

def test_revoked_token():
    revoked_file = "/app/revoked_tokens.txt"
    assert os.path.isfile(revoked_file), f"{revoked_file} is missing."
    with open(revoked_file, "r") as f:
        content = f.read()
    assert "TOKEN-9A8B7C6D5E4F" in content, "The compromised token was not found in revoked_tokens.txt."

def test_ssh_key_permissions_and_authorized_keys():
    admin_key = "/home/user/.ssh/admin_key"
    assert os.path.isfile(admin_key), f"{admin_key} is missing."
    st = os.stat(admin_key)
    assert stat.S_IMODE(st.st_mode) == 0o600, f"{admin_key} has incorrect permissions (expected 0600)."

    pub_key_file = admin_key + ".pub"
    assert os.path.isfile(pub_key_file), f"{pub_key_file} is missing."
    with open(pub_key_file, "r") as f:
        pub_key = f.read().strip()

    auth_keys = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys), f"{auth_keys} is missing."
    with open(auth_keys, "r") as f:
        auth_keys_content = f.read()

    assert pub_key.split()[1] in auth_keys_content, "The new public key was not found in authorized_keys."

def test_vendored_package_patched():
    login_py = "/app/vendored_auth/secure-auth-server-1.2.0/login.py"
    assert os.path.isfile(login_py), f"{login_py} is missing."
    with open(login_py, "r") as f:
        login_content = f.read()
    assert "http://" in login_content or "https://" in login_content or ".startswith('http')" in login_content or ".startswith(\"http\")" in login_content, "login.py does not appear to check for absolute URLs in the 'next' parameter."

    config_py = "/app/vendored_auth/secure-auth-server-1.2.0/config.py"
    assert os.path.isfile(config_py), f"{config_py} is missing."
    with open(config_py, "r") as f:
        config_content = f.read()
    assert "ValueError" in config_content or "os.environ['AUTH_KEY']" in config_content or 'os.environ["AUTH_KEY"]' in config_content, "config.py does not appear to be patched to raise ValueError when AUTH_KEY is missing."

def test_services_running():
    # Check if SSH is listening on 2222
    try:
        subprocess.run(["nc", "-z", "127.0.0.1", "2222"], check=True)
    except subprocess.CalledProcessError:
        assert False, "SSH server is not listening on 127.0.0.1:2222."

    # Check if HTTP server is listening on 8080
    try:
        subprocess.run(["nc", "-z", "127.0.0.1", "8080"], check=True)
    except subprocess.CalledProcessError:
        assert False, "HTTP server is not listening on 127.0.0.1:8080."

def test_http_server_redirects():
    # Test open redirect fix
    try:
        resp1 = requests.post("http://127.0.0.1:8080/login?next=http://evil.com", data={"username": "admin", "password": "password"}, allow_redirects=False)
        assert resp1.status_code in [301, 302, 303, 307, 308], f"Expected redirect status code, got {resp1.status_code}"
        assert resp1.headers.get("Location") == "/dashboard", f"Expected redirect to /dashboard for absolute URL, got {resp1.headers.get('Location')}"
    except requests.exceptions.RequestException as e:
        assert False, f"HTTP request failed: {e}"

    # Test relative redirect
    try:
        resp2 = requests.post("http://127.0.0.1:8080/login?next=/settings", data={"username": "admin", "password": "password"}, allow_redirects=False)
        assert resp2.status_code in [301, 302, 303, 307, 308], f"Expected redirect status code, got {resp2.status_code}"
        assert resp2.headers.get("Location") == "/settings", f"Expected redirect to /settings for relative URL, got {resp2.headers.get('Location')}"
    except requests.exceptions.RequestException as e:
        assert False, f"HTTP request failed: {e}"