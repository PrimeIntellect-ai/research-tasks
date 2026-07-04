# test_final_state.py

import os
import urllib.request
import ssl
import pytest

def test_shared_assets_logo():
    """Check that /home/user/shared_assets/logo.png exists and contains the correct data."""
    logo_path = "/home/user/shared_assets/logo.png"
    assert os.path.isfile(logo_path), f"File {logo_path} does not exist."
    with open(logo_path, "r") as f:
        content = f.read()
    assert content == "FAKE PNG DATA", f"Expected 'FAKE PNG DATA' in {logo_path}, got '{content}'"

def test_app_content_symlink():
    """Check that /home/user/app_content/assets is a symlink pointing to /home/user/shared_assets."""
    symlink_path = "/home/user/app_content/assets"
    target_path = "/home/user/shared_assets"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    actual_target = os.readlink(symlink_path)
    assert actual_target == target_path, f"Expected symlink {symlink_path} to point to {target_path}, but it points to {actual_target}."

def test_tls_certificates_exist():
    """Check that the TLS certificate and key exist."""
    crt_path = "/home/user/tls/server.crt"
    key_path = "/home/user/tls/server.key"
    assert os.path.isfile(crt_path), f"TLS certificate {crt_path} does not exist."
    assert os.path.isfile(key_path), f"TLS private key {key_path} does not exist."

def test_https_server_reachable():
    """Check that the HTTPS server is running and serving the logo.png file correctly."""
    url = "https://localhost:9443/assets/logo.png"

    # Create an unverified SSL context to simulate `curl -k`
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}"
            content = response.read().decode('utf-8')
            assert content == "FAKE PNG DATA", f"Expected response content 'FAKE PNG DATA', got '{content}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the HTTPS server at {url}: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while fetching {url}: {e}")